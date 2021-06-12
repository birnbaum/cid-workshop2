import subprocess
import sys
import os
import re
import pandas as pd
import xml.etree.ElementTree as ET


class mosaic_cid_tool:
    def __init__(self,
                 path_to_m: str,
                 sim_name: str,
                 is_unix: bool = True) -> None:
        """Initialize the path to MOSAIC and simulation name

        Parameters
        ----------
        path_to_m : str
            path to Eclipse MOSAIC
        sim_name : str
            Simulation name
        is_unix : bool
            Set True for UNIX based systems, set false for WINDOWS
        """
        self._path_to_m = path_to_m
        self._sim_name = sim_name

        self.is_unix = is_unix

    def _cd_mosaic(self):
        self.cwd = os.getcwd()
        os.chdir(self._path_to_m)

    def _std_pipe(self, command):
        sys.stdout.buffer.write(command.stdout)
        sys.stderr.buffer.write(command.stderr)
        # sys.exit(command.returncode)

    def run_simulation(self) -> None:
        """Run the selected simulation and record logs
        """
        self._cd_mosaic()
        extension = '.sh' if self.is_unix is True else '.bat'
        command = subprocess.run(['./mosaic' + extension,
                                  ' -s',
                                  self._sim_name + ' -v'],
                                 capture_output=True)
        self._std_pipe(command)

    def select_simulation_result(self, idx: int = 0):
        """Utility function to select the simulation and generate DataFrames
        IMPORTANT: Always run this function first after run_simulation() and
        before any other getter/setter and diverse functions!

        Parameters
        ----------
        idx : int, optional
            index of the log, 0 is the most recent result from
            the simulation, 1 is the second most recent, by default 0
        """
        log_path = self._path_to_m + 'logs/'
        dirs = sorted([f.name for f in os.scandir(log_path) if f.is_dir()],
                      reverse=True)
        self.sim_select = log_path + dirs[idx]

        output_root = self._get_output_config()

        # Create column names
        self.df_col_names = [re.sub(r"Updated:", '', i.text)
                             for i in output_root[0][3][0][0]]
        self.df_col_names = [re.sub(r"\.", '', i) for i in self.df_col_names]
        self.df_col_names[0] = 'Event'
        self.output_df = self._get_output_csv(self.df_col_names)

        return self.output_df

    def filter_df(self,
                  eventname: str,
                  app_name: str,
                  *args: str) -> pd.DataFrame:
        """Filter DataFrame using the event name, application name and
        fields

        Parameters
        ----------
        eventname : str
            Desired event name
        app_name : str
            Desired application name
        *args : str
            Fields to include in the filtered DataFrame

        Returns
        -------
        pd.DataFrame
            Filtered DataFrame
        """

        is_eventname = self.output_df.Event == eventname
        is_app_name = self.output_df.Name == app_name

        list_diff = list(set(self.df_col_names)
                         - set(args)
                         - set(['Event', 'Time', 'Name']))

        filtered_df = self.output_df[is_eventname
                                     & is_app_name].drop(list_diff, axis=1)

        return filtered_df

    def _get_output_csv(self, col_names) -> pd.DataFrame:
        """Getter function for the output.csv file, which holds the log data of
        the indexed simulation.

        Returns
        -------
        pd.DataFrame
            DataFrame of output.csv
        """
        return pd.read_csv(self.sim_select + '/output.csv',
                           sep=';',
                           header=None,
                           names=col_names)

    def _get_output_config(self):

        xml_path = self._path_to_m + 'scenarios/' + self.sim_name \
            + '/output/output_config.xml'

        tree = ET.parse(xml_path)
        return tree.getroot()

    @property
    def get_df_apps(self) -> list:
        """Getter DataFrame Applications

        Returns
        -------
        list
            DataFrame Applications
        """
        return sorted(list(set(self.output_df.Name)))

    @property
    def get_df_events(self) -> list:
        """Getter DataFrame Events

        Returns
        -------
        list
            DataFrame Events
        """

        return sorted(list(set(self.output_df.Event)))

    @property
    def get_df_labels(self) -> list:
        """Getter DataFrame Fields

        Returns
        -------
        list
            DataFrame Fields
        """
        return sorted(self.df_col_names)

    @property
    def get_output_df(self) -> pd.DataFrame:
        """Getter output DataFrame

        Returns
        -------
        pd.DataFrame
            output DataFrame
        """
        return self.output_df

    @property
    def sim_name(self) -> str:
        """Getter simulation name

        Returns
        -------
        str
            simulation name
        """
        return self._sim_name

    @sim_name.setter
    def sim_name(self, value: str) -> None:
        """Setter simulation name

        Parameters
        ----------
        value : simulation name
            value to set
        """
        self._sim_name = value
