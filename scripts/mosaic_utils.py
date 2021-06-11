import subprocess
import sys
import os
import pandas as pd


class mosaic_utils:
    def __init__(self, path_to_m: str, sim_name: str) -> None:
        self._path_to_m = path_to_m
        self._sim_name = sim_name

        self._cd_mosaic()

    def _cd_mosaic(self):
        self.cwd = os.getcwd()
        os.chdir(self._path_to_m)

    def _std_pipe(self, command):
        sys.stdout.buffer.write(command.stdout)
        sys.stderr.buffer.write(command.stderr)
        # sys.exit(command.returncode)1

    def run_simulation(self):
        command = subprocess.run(['./mosaic.sh', '-s', self._sim_name + ' -v'],
                                 capture_output=True)

        self._std_pipe(command)

    def change_xml(self):
        pass

    def change_setting(self):
        pass

    def select_simulation_result(self, idx: int = 0, colnum: int = 11):
        """
        Utility function to select the simulation and generate DataFrames

        idx : int
            index of the log, 0 is the most recent result from
            the simulation, 1 is the second most recent

        colnum : int
            Number of columns, default 11
        """
        log_path = self._path_to_m + 'logs/'
        dirs = sorted([f.name for f in os.scandir(log_path) if f.is_dir()],
                      reverse=True)
        self.sim_select = log_path + dirs[idx]
        self.colnum = [i for i in range(colnum)]
        
        self._get_output_csv()

    def _get_output_csv(self):
        """
        Getter function for the output.csv file, which holds the log data of
        the indexed simulation.
        """
        self.output_df = pd.read_csv(self.sim_select + '/output.csv',
                                     sep=';',
                                     header=None,
                                     names=self.colnum)

    @property
    def sim_name(self):
        return self._sim_name

    @sim_name.setter
    def sim_name(self, value):
        self._sim_name = value


def main():
    mosaic = mosaic_utils('/home/onqi/Documents/eclipse_mosaic/', 'Barnim')
    # mosaic.run_simulation()
    mosaic.select_simulation_result(idx=0, colnum=30)
    pass


if __name__ == '__main__':
    main()
