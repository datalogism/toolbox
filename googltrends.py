# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16 15:38:23 2019

@author: Celian
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Feb  7 23:41:06 2019

@author: Celian
"""


from pytrends.request import TrendReq
import pandas as pd
import requests
keyword="fievre"
country="FR"
### BENIN BONHEUR
df=None
pytrends = TrendReq(hl='fr-FR', tz=1)
pytrends.interest_by_region(resolution='REGION')
pytrends.build_payload([keyword], cat=0, timeframe='2017-01-01 2017-12-31', geo='FR', gprop='')
res=pytrends.interest_over_time()
res=pytrends.get_historical_interest([keyword], year_start=2019, month_start=1, day_start=1, hour_start=0, year_end=2019, month_end=5, day_end=15, hour_end=0, cat=0, geo='FR-M', gprop='', sleep=0)