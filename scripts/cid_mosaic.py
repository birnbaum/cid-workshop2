import subprocess
import sys
import os
import re
import json
from lxml import etree

import numpy as np
import pandas as pd
import glom
import matplotlib.pyplot as plt
import pyproj
from matplotlib.collections import LineCollection

from typing import Any


try:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
    import sumolib
except ImportError:
    sys.exit("please declare environment variable 'SUMO_HOME'")


class cid_mosaic:
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
    def __init__(self,
                 path_to_m: str,
                 sim_name: str,
                 is_unix: bool = True) -> None:
        self._path_to_m = path_to_m
        self._sim_name = sim_name

        self.is_unix = is_unix

        self._cd_mosaic()

    def _cd_mosaic(self):
        os.chdir(self._path_to_m)
        self.cwd = os.getcwd()

    def _std_pipe(self, command):
        sys.stdout.buffer.write(command.stdout)
        sys.stderr.buffer.write(command.stderr)
        # sys.exit(command.returncode)

    def run_simulation(self, jupyter=False) -> None:
        """Run the selected simulation and record logs
        """
        extension = '.sh' if self.is_unix is True else '.bat'
        if jupyter is False:
            command = subprocess.run(['./mosaic' + extension,
                                      ' -s',
                                      self._sim_name + ' -v'],
                                     capture_output=True)
            self._std_pipe(command)
            return 0
        else:
            cmd = './mosaic' + extension + ' -s' \
                + self.sim_name + ' -v'
            return cmd

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
        log_path = os.path.join('.', 'logs')
        dirs = sorted([f.name for f in os.scandir(log_path) if f.is_dir()],
                      reverse=True)
        self.sim_select = os.path.join(log_path, dirs[idx])

        output_root = self._get_output_config()

        id2fields = dict()
        for elem in output_root[0][3]:
            k = elem.attrib['id']
            v = [re.sub(r"Updated:", '', i.text) for i in elem[0]]
            v = [re.sub(r"\.", '', i) for i in v]
            v[0] = 'Event'
            id2fields[k] = v

        self.id2fields = id2fields

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
        col_names = self.id2fields[eventname]

        reg_eventname = re.sub(r'(?=[A-Z])', '_', eventname)
        reg_eventname = reg_eventname.replace('_', '', 1)
        eventname = reg_eventname.upper()

        output_df = self._get_output_csv(col_names)

        is_eventname = output_df.Event == eventname
        
        app_names = ['Name', 'MappingName', 'ReceiverName', 'SourceName']
        try:
            is_app_name = output_df.Name == app_name
            app_name = 'Name'
        except AttributeError:
            try:
                is_app_name = output_df.MappingName == app_name
                app_name = 'MappingName'
            except AttributeError:
                try:
                    is_app_name = output_df.ReceiverName == app_name
                    app_name = 'ReceiverName'
                except AttributeError:
                    try:
                        is_app_name = output_df.MappingName == app_name
                        app_name = 'SourceName'
        finally:
            pass

        if args[0] != 'all':
            list_diff = list(set(col_names)
                             - set(args)
                             - set(['Event', 'Time', app_name]))

            filtered_df = output_df[is_eventname
                                    & is_app_name].drop(list_diff, axis=1)
        else:
            filtered_df = output_df[is_eventname & is_app_name]

        return filtered_df

    def _get_output_csv(self, col_names) -> pd.DataFrame:
        """Getter function for the output.csv file, which holds the log data of
        the indexed simulation.

        Returns
        -------
        pd.DataFrame
            DataFrame of output.csv
        """
        return pd.read_csv(os.path.join(self.sim_select + '/output.csv'),
                           sep=';',
                           header=None,
                           names=col_names)

    def _get_output_config(self):

        xml_path = os.path.join('.',
                                'scenarios',
                                self._sim_name,
                                'output',
                                'output_config.xml')

        tree = etree.parse(xml_path)
        return tree.getroot()

    def df2np(self, df: pd.DataFrame) -> np.array:
        """Convert DataFrame to Numpy array

        Parameters
        ----------
        df : pd.DataFrame
            Input DataFrame

        Returns
        -------
        np.array
            np.asfarray(df1)
        """
        return np.asfarray(df)

    def retrieve_federate(self, federate: str, idx=None) -> str:
        """Retrieves the selected federate and initializes object attribute for
        further actions

        Parameters
        ----------
        federate : str
            Federate name, can be 'scenario' or any of the other federates,
            i.e. 'application', 'sns', 'cell', etc.
        idx : int, optional
            Index of the federate within a federate folder, if idx=None, no
            federate is selected and available options are displayed

        Returns
        -------
        str
            Full path of the federate json
        """

        if federate == 'scenario':
            path_to_fedjson = os.path.join('.',
                                           'scenarios',
                                           self._sim_name,
                                           'scenario_config.json')
            self.fed_path = path_to_fedjson
            foo = open(path_to_fedjson)
            self.fed_name = 'scenario_config.json'
            self.current_fed_setting = json.load(foo)
            return path_to_fedjson

        else:
            path_to_json = os.path.join('.',
                                        'scenarios',
                                        self._sim_name,
                                        federate)

            json_files = sorted([pos_json for pos_json
                                 in os.listdir(path_to_json)
                                 if pos_json.endswith('.json')])

            if idx is None:
                print(json_files)
                return json_files
            else:
                assert isinstance(idx, int)
                path_to_fedjson = os.path.join(path_to_json, json_files[idx])
                self.fed_path = path_to_fedjson
                foo = open(path_to_fedjson)
                self.fed_name = json_files[idx]
                self.current_fed_setting = json.load(foo)
                return path_to_fedjson

    def set_federate_value(self, tree: str, value: str) -> None:
        """Sets the selected federate value in the tree and dumps the new
        federate configuration into JSON

        Parameters
        ----------
        tree : str
            dict tree to navigate to the federate value to be changed, i.e.
            'globalNetwork.uplink.delay.delay'
        value : str
            value to set, IMPORTANT: make sure you follow the format of the
            federate value
        """
        glom.assign(self.current_fed_setting, tree, val=value)
        print('Federate value of {} set to {}'.format(
            tree, value
        ))
        with open(self.fed_path, 'w') as f:
            json.dump(self.current_fed_setting, f, indent=4)
        pass

    def get_federate_value(self, tree: str) -> Any:
        """Gets the selected federate value in the tree

        Parameters
        ----------
        tree : str
            dict tree to navigate to the federate value to be changed, i.e.
            'globalNetwork.uplink.delay.delay'

        Returns
        -------
        Any
            federate value
        """

        return glom.glom(self.current_fed_setting, tree)

    @property
    def pprint_curr_fed(self):
        """Pretty print current federate configuration
        """
        print('Current federate: {}'.format(self.fed_name))
        print(json.dumps(self.current_fed_setting, indent=4, sort_keys=True))

    @property
    def get_federates(self):
        """Print available federate configurations
        """
        path_to_settings = os.path.join('.',
                                        'scenarios',
                                        self._sim_name)
        print('Available federates: {}'.format(sorted(
            [f.name for f in os.scandir(path_to_settings)])))

    @property
    def get_df_apps(self) -> list:
        """Getter DataFrame Applications

        Returns
        -------
        list
            DataFrame Applications
        """
        app_dir = os.path.join(self.sim_select, 'apps')
        return sorted([f.name for f in os.scandir(app_dir) if f.is_dir()], reverse=True)

    @property
    def get_df_events(self) -> list:
        """Getter DataFrame Events

        Returns
        -------
        list
            DataFrame Events
        """

        return list(self.id2fields.keys())

    def get_df_labels(self, event: str) -> list:
        """Getter DataFrame Fields

        Parameters
        ----------
        event : str
            Event type

        Returns
        -------
        list
            DataFrame Fields
        """
        return self.id2fields[event]

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

    def plotter(self) -> None:
        path_net = os.path.join('.',
                                'scenarios',
                                'Barnim',
                                'sumo',
                                'Barnim.net.xml')

        net = sumolib.net.readNet(path_net)
        x_off, y_off = net.getLocationOffset()

        p = pyproj.Proj(proj='utm',
                        zone=33,
                        ellps='WGS84',
                        preserve_units=False)

        fig, ax = plt.subplots()
        shapes = [elem.getShape() for elem in net._edges]

        shapes_geo = []

        for shape in shapes:
            foo = [(p(el[0] - x_off, el[1] - y_off,
                      inverse=True)) for el in shape]
            shapes_geo.append(foo)

        line_segments = LineCollection(shapes_geo)
        ax.add_collection(line_segments)
        ax.set_xmargin(0.1)
        ax.set_ymargin(0.1)
        ax.autoscale_view(True, True, True)
        ax.set_ylim([52.60, 52.66])
        ax.set_xlim([13.51, 13.60])

        # Add RSUs
        rsu_0 = 0
