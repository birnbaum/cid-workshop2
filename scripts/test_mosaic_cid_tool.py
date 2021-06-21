from cid_mosaic import cid_mosaic
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def main():
    sns.set()
    mosaic = cid_mosaic('/home/onqi/Documents/eclipse_mosaic/',
                        'Barnim')
    # mosaic.run_simulation()
    mosaic.select_simulation_result()
    """
    print(mosaic.get_df_labels)
    print(mosaic.get_df_events)
    print(mosaic.get_df_apps)

    veh0 = mosaic.filter_df('VEHICLE_UPDATES', 'veh_0', 'all')
    veh1 = mosaic.filter_df('VEHICLE_UPDATES', 'veh_1', 'all')
    veh2 = mosaic.filter_df('VEHICLE_UPDATES', 'veh_2', 'all')


    # pd.DataFrame to np.array

    plt.figure()
    plt.plot(np.asfarray(veh0.Time), np.asfarray(veh0.Speed), label='veh0')
    plt.plot(np.asfarray(veh1.Time), np.asfarray(veh1.Speed), label='veh1')
    plt.plot(np.asfarray(veh2.Time), np.asfarray(veh2.Speed), label='veh2')
    plt.title('Speed of Vehicle 0-1-2')
    plt.legend()

    plt.figure()
    plt.scatter(np.asfarray(veh0.PositionLatitude),
                np.asfarray(veh0.PositionLongitude),
                linewidths=0.5,
                label='veh0')
    plt.scatter(np.asfarray(veh1.PositionLatitude),
                np.asfarray(veh1.PositionLongitude),
                linewidths=0.5,
                label='veh1')
    plt.scatter(np.asfarray(veh2.PositionLatitude),
                np.asfarray(veh2.PositionLongitude),
                linewidths=0.5,
                label='veh2')
    plt.title('Road Travelled - Vehicle 0-1-2')
    plt.legend()

    plt.show()

    # print(mosaic.get_settings)
    mosaic.get_federates
    mosaic.retrieve_federate('cell', idx=1)
    mosaic.pprint_curr_fed

    mosaic.set_federate_value('globalNetwork.uplink.delay.delay',
                              '100 ms')
    """

    # veh0 = mosaic.filter_df('VEHICLE_UPDATES', 'veh_0', 'all')
    # test_df = mosaic.filter_df('RsuRegistration', 'rsu_0', 'all')

    """

    veh0 = mosaic.filter_df(Event='VEHICLE_UPDATES', Name='veh_0', select='all')

    rsu0 = mosaic.filter_df(Event='RSU_REGISTRATION',
                            MappingName='rsu_0',
                            select=['MappingPositionLatitude',
                                    'MappingPositionLongitude'])
    """

    mosaic.plotter()
    plt.show()

    pass


if __name__ == '__main__':
    main()
