from mosaic_cid_tool import mosaic_cid_tool


def main():
    mosaic = mosaic_cid_tool('/home/onqi/Documents/eclipse_mosaic/', 'Barnim')
    mosaic.run_simulation()
    mosaic.select_simulation_result()
    print(mosaic.get_df_labels)
    print(mosaic.get_df_events)
    print(mosaic.get_df_apps)

    filtered_df = mosaic.filter_df('VEHICLE_UPDATES',
                                   'veh_2',
                                   'Speed',
                                   'Heading')

    filtered_df2 = mosaic.filter_df('VEHICLE_UPDATES',
                                    'veh_2',
                                    'Speed',
                                    'PositionLongitude')

    pass


if __name__ == '__main__':
    main()
