Order of worship is generated with:
```
% liturgist --date 2025-01-12 --bible-json-path samples/kjv.json --template samples/order-of-worship.html samples/schedule.csv
```

### Google Sheets

After configuring `rclone`, you can download schedule google sheets as an excel spreadsheet
```
% rclone copyto "gdrive:schedule.xlsx" ./schedule.xlsx
% python liturgist.py schedule.xlsx --date 01/05/25 --print-json
```
