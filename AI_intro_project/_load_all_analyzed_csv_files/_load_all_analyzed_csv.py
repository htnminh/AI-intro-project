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
    print('A*'.center(80), file=fo)
    print('-' * length_count, file=fo)
    rbfs_csv_path = r'AI_intro_project\search_algo\load_all_output\output-rbfs.csv'
    df_rbfs = pd.read_csv(rbfs_csv_path, header=0)
    print(df_rbfs.describe(), file=fo)


df_rbfs.sort_values(by='idx', inplace=True)
df_dfs.sort_values(by='idx', inplace=True)
df_astar.sort_values(by='idx', inplace=True)