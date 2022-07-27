
from processing.datasetConstructor import *

file_rows = [[0,1,2], [3,4,5], [6,7,8]]
features_file = create_file("processing/features_file.csv")

features_file.write_lines_on_file(file_rows)



