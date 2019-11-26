# Weekly-process
weekly-process include check_csv.py,process.py and diff_modules.py:

      check_csv.py:check the data and fix it
      process.py:get statistics.csv,emolt_no_telemetry.csv,time_series_plot and location map of vessel
      diff_modules.py:get weekly.html
The parameter of Weekly process should include raw_data_name.txt , telemetry_status.csv and dictionary.json 3 parts:
      
      raw_data_name.txt:If wouldn't add new vessel,we don't need to change
      telemetry_status.csv: Before run WeeklyProcess,downloaded from https://docs.google.com/spreadsheets/d/1uLhG_q09136lfbFZppU2DU9lzfYh0fJYsxDHUgMB1FM/edit?ts=5ba8fe2b#gid=0 as a "tab-delimited comma-delimited and "-delimited" csv file
      dictionary.json: receive from Jim every week
Nov 14,2019

update match_tele_raw/raw_tele_modules.py to count number boats in statistics.csv by adding the key of tele_total_num

Nov 25,2019

update match_tele_raw/raw_tele_modules.py:By creating emolt_raw.csv to compares with emolt.dat and got the absent of  emolt.dat named emolt_no_telemetry.csv
