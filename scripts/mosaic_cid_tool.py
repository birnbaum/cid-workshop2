import subprocess
import sys
import os
import re
import pandas as pd
import xml.etree.ElementTree as ET


class mosaic_cid_tool:
    def __init__(self, path_to_m: str, sim_name: str) -> None:
        """Initialize the path to MOSAIC and simulation name

        Parameters
        ----------
        path_to_m : str
            path to Eclipse MOSAIC
        sim_name : str
            Simulation name
        """
        self._path_to_m = path_to_m
        self._sim_name = sim_name

        self._cd_mosaic()

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
        command = subprocess.run(['./mosaic.sh', '-s', self._sim_name + ' -v'],
                                 capture_output=True)

        self._std_pipe(command)

    def select_simulation_result(self, idx: int = 0):
        """Utility function to select the simulation and generate DataFrames

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

    def filter_df(self, eventname: str, app_name: str, *args: str):

        is_eventname = self.output_df.Event == eventname
        is_app_name = self.output_df.Name == app_name

        list_diff = list(set(self.df_col_names) - set(args) - set(['Event', 'Time', 'Name']))

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
    def get_df_labels(self) -> list:
        """Getter DataFrame fields and event names

        Returns
        -------
        list
            DataFrame labels
        """
        return self.df_col_names

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
    def sim_name(self):
        return self._sim_name

    @sim_name.setter
    def sim_name(self, value):
        self._sim_name = value


def main():
    mosaic = mosaic_cid_tool('/home/onqi/Documents/eclipse_mosaic/', 'Barnim')
    # mosaic.run_simulation()
    mosaic.select_simulation_result()
    print(mosaic.get_df_labels)

    filtered_df = mosaic.filter_df('VEHICLE_UPDATES', 'veh_2', 'Speed')

    pass


if __name__ == '__main__':
    main()
