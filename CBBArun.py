import json
import matplotlib.pyplot as plt
import pathmagic
with pathmagic.context():
    from CBBA import CBBA
    from WorldInfo import WorldInfo
    import HelperLibrary as HelperLibrary
import time

if __name__ == "__main__":
    time_s=time.time()
    # a json configuration file
    config_file_name = "package.json"
    # Read the configuration from the json file
    json_file = open(config_file_name)
    config_data = json.load(json_file)

    # create a world, each list is [min, max] coordinates for x,y,z axis
    WorldInfoTest = WorldInfo([-2.0, 2.5], [-1.5, 5.5], [0.0, 20.0])

    # create a list of Agent(s) and Task(s)
    num_agents = 5
    num_tasks = 10
    max_depth =2
    #*************************************需要修改的地方
    AgentList, TaskList = HelperLibrary.create_agents_and_tasks(num_agents, num_tasks, WorldInfoTest, config_data)
    # AgentList,TaskList = HelperLibrary.create_set(num_agents,num_tasks,WorldInfoTest,config_data)
    # create a CBBA solver
    CBBA_solver = CBBA(config_data)


    # solve
    path_list, times_list = CBBA_solver.solve(AgentList, TaskList, WorldInfoTest, max_depth, time_window_flag=True)

#**************************************************************
    # path_list is a 2D list, i-th sub-list is the task exploration order of Agent-i.
    # e.g. path_list = [[0, 4, 3, 1], [2, 5]] means Agent-0 visits Task 0 -> 4 -> 3 -> 1, and Agent-1 visits Task 2 -> 5

    # times_list is a 2D list, i-th sub-list is the task beginning timestamp of Agent-i's tasks.
    # e.g. times_list = [[10.5, 20.3, 30.0, 48.0], [20.4, 59.5]] means Agent-0 arrives at Task-0 before time=10.5 second, and then conduct Task-0;
    # Agent-0 arrives at Task-4 before time=20.3 second, and then conduct Task-4, etc.
#*************************************
    #plot  time window
    CBBA_solver.plot_assignment()
    plt.show()
#**************************************

    #没有task-time window
    AgentList, TaskList = HelperLibrary.create_agents_and_tasks_homogeneous(num_agents, num_tasks, WorldInfoTest,
                                                                            config_data)
    # create a CBBA solver
    CBBA_solver = CBBA(config_data)

    # solve, no time window
    path_list, _ = CBBA_solver.solve(AgentList, TaskList, WorldInfoTest, max_depth, time_window_flag=False)
    # plot no time window
    CBBA_solver.plot_assignment_without_timewindow()
    plt.show()
    time_e = time.time()
    sum = time_e - time_s
    print("总运行时间: ", sum)