import runner_final_experiment_two

possibles_names_average = ['policy_average_7x7','policy_average_3x3','baseline_average_7x7','baseline_average_3x3',
             'intention_average_7x7','intention_average_3x3','MORL_average_7x7','MORL_average_3x3','goal_average_3x3'
                   ,'goal_average_7x7']
possibles_names_complex = ['policy_complex_7x7','policy_complex_3x3','baseline_complex_7x7','baseline_complex_3x3',
             'intention_complex_7x7','intention_complex_3x3','MORL_complex_7x7','MORL_complex_3x3','goal_complex_3x3'
                   ,'goal_complex_7x7']

possibles_names_average = ["MORL_average_7x7","MORL_average_3x3","goal_average_3x3","goal_average_7x7"]
possibles_names_complex = ["goal_complex_7x7","goal_complex_3x3","MORL_complex_7x7","MORL_complex_3x3"]




def save(file,name):
    file.write("import runner_final_experiment_two\n")
    file.write("runner_final_experiment_two.run_experiment(world_name="+"'"+name+"')")
    file.close()
count=1
for i in possibles_names_average:
    save(open("runner_exp_three_"+str(count)+".py",'w'), i)
    print(i,count)
    count+=1
for j in possibles_names_complex:
    save(open("runner_exp_three_" + str(count) + ".py", 'w'), j)
    print(j,count)
    count+=1

