CREATE TABLE prices 
(
symbol TEXT,
day DATE,

open REAL,
close REAL,
high REAL,
low REAL,
volume INTEGER,

PRIMARY KEY (symbol, day)
);