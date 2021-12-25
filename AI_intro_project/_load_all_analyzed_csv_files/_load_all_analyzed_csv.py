from numpy import true_divide
import pandas as pd
import matplotlib.pyplot as plt

pd.reset_option("all")


length_count = 81
output_dir = r'AI_intro_project\_load_all_analyzed_csv_files'
output_txt_path = output_dir + r'\_load_all_analyzed_csv.txt'


with open(output_txt_path, 'w') as fo:
    print('-' * length_count, file=fo)
    print('DFS'.center(80), file=fo)
    print('-' * length_count, file=fo)
    dfs_csv_path = r'AI_intro_project\search_algo\load_all_output\output-dfs.csv'
    df_dfs = pd.read_csv(dfs_csv_path, header=0)
    print(df_dfs.describe(), file=fo)

    print('-' * length_count, file=fo)
    print('A*'.center(80), file=fo)
    print('-' * length_count, file=fo)
    astar_csv_path = r'AI_intro_project\search_algo\load_all_output\output-astar.csv'
    df_astar = pd.read_csv(astar_csv_path, header=0)
    print(df_astar.describe(), file=fo)

    print('-' * length_count, file=fo)
    print('RBFS'.center(80), file=fo)
    print('-' * length_count, file=fo)
    rbfs_csv_path = r'AI_intro_project\search_algo\load_all_output\output-rbfs.csv'
    df_rbfs = pd.read_csv(rbfs_csv_path, header=0)
    print(df_rbfs.describe(), file=fo)


df_rbfs.sort_values(by='idx', inplace=True)
df_dfs.sort_values(by='idx', inplace=True)
df_astar.sort_values(by='idx', inplace=True)

df_merge = df_dfs.copy()
df_astar_t = df_astar.copy()

df_astar_t.columns = ['idx', *[i + "_astar" for i in df_astar_t if i != 'idx']]
df_merge = df_merge.join(df_rbfs, lsuffix='_dfs', rsuffix='_rbfs', on='idx')
df_merge = df_merge.join(df_astar_t)

###############
df_merge.plot(x='idx', y=['ram_usage_dfs', 'ram_usage_rbfs', 'ram_usage_astar'])
plt.title('RAM Usage per board')
plt.savefig(rf'{output_dir}\analysis\S3-RAM-light')

df_merge.plot(x='idx', y=['time_dfs', 'time_rbfs', 'time_astar'])
plt.title('Running time per board')
plt.savefig(rf'{output_dir}\analysis\S3-TIME-light')

df_merge.plot(x='idx', y=['iteration_dfs', 'iteration_rbfs', 'iteration_astar'])
plt.title('Total Number of Iterations per board')
plt.savefig(rf'{output_dir}\analysis\S3-ITER-light')

###############
df_dfs.plot(x='idx', y=['time', 'iteration'], subplots=True)
plt.title('Relation between Iteration and Time - DFS')
plt.savefig(rf'{output_dir}\analysis\DFS-Time-light')

df_rbfs.plot(x='idx', y=['time', 'iteration'], subplots=True)
plt.title('Relation between Iteration and Time - RBFS')
plt.savefig(rf'{output_dir}\analysis\RBFS-Time-light')

df_astar.plot(x='idx', y=['time', 'iteration'], subplots=True)
plt.title('Relation between Iteration and Time - A*')
plt.savefig(rf'{output_dir}\analysis\A-Time-light')