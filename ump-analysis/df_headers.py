def df_headers(source: str) -> list:
    headers = []
    match source:
        case 'statcast':
            headers = ['pitch_type', 'game_date', 'release_speed', 'release_pos_x',
            'release_pos_z', 'player_name', 'batter', 'pitcher', 'events',
            'description', 'spin_dir', 'spin_rate_deprecated',
            'break_angle_deprecated', 'break_length_deprecated', 'zone', 'des',
            'game_type', 'stand', 'p_throws', 'home_team', 'away_team', 'type',
            'hit_location', 'bb_type', 'balls', 'strikes', 'game_year', 'pfx_x',
            'pfx_z', 'plate_x', 'plate_z', 'on_3b', 'on_2b', 'on_1b',
            'outs_when_up', 'inning', 'inning_topbot', 'hc_x', 'hc_y',
            'tfs_deprecated', 'tfs_zulu_deprecated', 'fielder_2', 'umpire', 'sv_id',
            'vx0', 'vy0', 'vz0', 'ax', 'ay', 'az', 'sz_top', 'sz_bot',
            'hit_distance_sc', 'launch_speed', 'launch_angle', 'effective_speed',
            'release_spin_rate', 'release_extension', 'game_pk', 'pitcher.1',
            'fielder_2.1', 'fielder_3', 'fielder_4', 'fielder_5', 'fielder_6',
            'fielder_7', 'fielder_8', 'fielder_9', 'release_pos_y',
            'estimated_ba_using_speedangle', 'estimated_woba_using_speedangle',
            'woba_value', 'woba_denom', 'babip_value', 'iso_value',
            'launch_speed_angle', 'at_bat_number', 'pitch_number', 'pitch_name',
            'home_score', 'away_score', 'bat_score', 'fld_score', 'post_away_score',
            'post_home_score', 'post_bat_score', 'post_fld_score',
            'if_fielding_alignment', 'of_fielding_alignment', 'spin_axis',
            'delta_home_win_exp', 'delta_run_exp']
        case 'retrosheet-events':
            headers = ['game_id', 'visiting_team', 'inning', 'batting_team', 'outs',
            'balls', 'strikes', 'pitch_sequence', 'vis_score', 'home_score', 'batter',
            'batter_hand', 'res_batter', 'res_batter_hand','pitcher', 'pitcher_hand',
            'res_pitcher', 'res_pitcher_hand','catcher', 'first_base', 'second_base',
            'third_base', 'shortstop', 'left_field', 'center_field', 'right_field',
            'first_runner', 'second_runner', 'third_runner', 'event_text',
            'leadoff_flag', 'pinchhit_flag', 'defensive_position', 'lineup_position',
            'event_type', 'batter_event_flag', 'ab_flag', 'hit_value', 'sh_flag',
            'sf_flag', 'outs_on_play', 'double_play_flag', 'triple_play_flag',
            'rbi_on_play', 'wild_pitch_flag', 'passed_ball_flag', 'fielded_by',
            'batted_ball_type', 'bunt_flag', 'foul_flag', 'hit_location',
            'num_errors', '1st_error_player', '1st_error_type', '2nd_error_player',
            '2nd_error_type', '3rd_error_player', '3rd_error_type', 'batter_dest',
            'runner_on_1st_dest', 'runner_on_2nd_dest', 'runner_on_3rd_dest',
            'play_on_batter', 'play_on_runner_on_1st', 'play_on_runner_on_2nd',
            'play_on_runner_on_3rd', 'sb_for_runner_on_1st_flag',
            'sb_for_runner_on_2nd_flag', 'sb_for_runner_on_3rd_flag',
            'cs_for_runner_on_1st_flag', 'cs_for_runner_on_2nd_flag',
            'cs_for_runner_on_3rd_flag', 'po_for_runner_on_1st_flag',
            'po_for_runner_on_2nd_flag', 'po_for_runner_on_3rd_flag',
            'responsible_pitcher_for_runner_on_1st',
            'responsible_pitcher_for_runner_on_2nd',
            'responsible_pitcher_for_runner_on_3rd','new_game_flag','end_game_flag',
            'pinch-runner_on_1st?', 'pinch-runner_on_2nd?', 'pinch-runner_on_3rd?',
            'id_of_runner_removed_for_pinch-runner_on_1st',
            'id_of_runner_removed_for_pinch-runner_on_2nd',
            'id_of_runner_removed_for_pinch-runner_on_3rd',
            'id_of_batter_removed_for_pinch-hitter',
            'fielding_position_of_batter_removed_for_pinch-hitter',
            'fielder_with_first_putout', 'fielder_with_second_putout',
            'fielder_with_third_putout', 'fielder_with_first_assist',
            'fielder_with_second_assist', 'fielder_with_third_assist',
            'fielder_with_fourth_assist', 'fielder_with_fifth_assist','event_num']
        case 'retrosheet-games':
            headers = ['game_id', 'date', 'game_number', 'day_of_week', 'start_time',
            'dh_used_flag', 'day_night_flag', 'visiting_team', 'home_team','game_site',
            'visiting_starting_pitcher', 'home_starting_pitcher', 'home_plate_umpire',
            'first_base_umpire', 'second_base_umpire', 'third_base_umpire',
            'left_field_umpire', 'right_field_umpire', 'attendance', 'PS_scorer',
            'translator', 'inputter', 'input_time', 'edit_time', 'how_scored',
            'pitches_entered', 'temperature', 'wind_direction', 'wind_speed',
            'field_condition', 'precipitation', 'sky', 'time_of_game',
            'number_of_innings', 'visitor_final_score', 'home_final_score',
            'visitor_hits', 'home_hits', 'visitor_errors', 'home_errors',
            'visitor_left_on_base', 'home_left_on_base', 'winning_pitcher',
            'losing_pitcher', 'save_for', 'gw_rbi', 'visitor_batter_1',
            'visitor_position_1', 'visitor_batter_2', 'visitor_position_2',
            'visitor_batter_3', 'visitor_position_3', 'visitor_batter_4',
            'visitor_position_4', 'visitor_batter_5', 'visitor_position_5',
            'visitor_batter_6', 'visitor_position_6', 'visitor_batter_7',
            'visitor_position_7', 'visitor_batter_8', 'visitor_position_8',
            'visitor_batter_9', 'visitor_position_9', 'home_batter_1',
            'home_position_1', 'home_batter_2', 'home_position_2', 'home_batter_3',
            'home_position_3', 'home_batter_4', 'home_position_4', 'home_batter_5',
            'home_position_5', 'home_batter_6', 'home_position_6', 'home_batter_7',
            'home_position_7', 'home_batter_8', 'home_position_8', 'home_batter_9',
            'home_position_9', 'gametype']
        case 're288-index':
            headers = ['0 123', '0 _23', '0 1_3', '0 __3', '0 12_', '0 _2_', '0 1__', '0 ___',
            '1 123', '1 _23', '1 1_3', '1 __3', '1 12_', '1 _2_', '1 1__', '1 ___',
            '2 123', '2 _23', '2 1_3', '2 __3', '2 12_', '2 _2_', '2 1__', '2 ___']
        case 're288-columns':
            headers = ['[0-0]', '[0-1]', '[0-2]', '[1-0]', '[1-1]', '[1-2]', '[2-0]', '[2-1]', '[2-2]', '[3-0]','[3-1]', '[3-2]']
    return headers