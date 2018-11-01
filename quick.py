import quick_run
possibles_names_average = ['policy_average_7x7','policy_average_3x3','baseline_average_7x7','baseline_average_3x3',
             'intention_average_7x7','intention_average_3x3','MORL_average_7x7','MORL_average_3x3','goal_average_3x3'
                   ,'goal_average_7x7','centralized_average_entire']

possibles_names_complex = ['policy_complex_7x7','policy_complex_3x3','baseline_complex_7x7','baseline_complex_3x3',
             'intention_complex_7x7','intention_complex_3x3','MORL_complex_7x7','MORL_complex_3x3','goal_complex_3x3'
                   ,'goal_complex_7x7','centralized_complex_entire']

quick_run.run_experiment("intention_average_7x7")