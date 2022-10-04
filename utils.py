from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time 


def collect_fight_info(driver_, data_):
   flag = 0
   title = False

   results_ = driver_.find_element(By.XPATH, "//div[@class='b-fight-details__persons clearfix']").text.split('\n')

   for idx, element in enumerate(results_):
      if element == 'W':
         if flag == 0:
            red_fighter = results_[idx+1]
            data_['result'] = red_fighter
            flag = 1
         else:
            blue_fighter = results_[idx+1]
            data_['result'] = blue_fighter
      elif element == 'L':
         if flag == 0:
            red_fighter = results_[idx+1]
            flag = 1 
         else:
            blue_fighter = results_[idx+1]
      elif element == 'D':
         data_['result'] = 'D'
         if flag == 0:
            red_fighter = results_[idx+1]
            flag = 1
         else:
            blue_fighter = results_[idx+1]
            
   data_['red_fighter'] = red_fighter
   data_['blue_fighter'] = blue_fighter

   fight_details = driver_.find_element(By.XPATH, "//div//i[@class='b-fight-details__fight-title']").text.split(' ')

   for idx, details in enumerate(fight_details):
      if 'WEIGHT' in details:
         if 'WEIGHT' == details:
               data_['weight_class'] = fight_details[idx-1] + ' ' + details
         else:
               data_['weight_class'] = details

      if ('TITLE' in details and not title):
         data_['title_fight'] = 1
      else:
         data_['title_fight'] = 0

   data_['event'] = driver_.find_element(By.XPATH, "//a[@class='b-link']").text

   test = driver_.find_elements(By.XPATH, "//div[@class='b-fight-details__content']//p[@class='b-fight-details__text']//i[@class='b-fight-details__text-item']")
   first = driver_.find_elements(By.XPATH, "//div[@class='b-fight-details__content']//p[@class='b-fight-details__text']//i[@class='b-fight-details__text-item_first']")

   method_data = first[0].text.split(': ')
   round_data = test[0].text.split(': ')
   time_data = test[1].text.split(': ')
   time_format_data = test[2].text.split(': ')
   referee_data = test[3].text.split(': ')

   data_['method'] = method_data[-1]
   data_['round'] = round_data[-1]
   data_['time'] = time_data[-1]
   data_['round_format'] = time_format_data[-1]
   data_['referee'] = referee_data[-1]

   return data_ 

def get_result(driver_):
    result_list = driver_.find_element(By.XPATH, "//div[@class='b-fight-details__persons clearfix']").text.split('\n')
    for idx, result in enumerate(result_list):
        if result == 'W':
            win_idx = idx + 1
    return result_list[win_idx]

def split_fight_stats(data_):
    new_strike_data = []
    
    for data in data_:
        if 'of' in data:
            new_strike_data += [i.strip() for i in data.split('of')]
        else:
            new_strike_data.append(data)
    return new_strike_data

def collect_fight_stats(driver_):
    fight_data_ = driver_.find_elements(By.XPATH, "//tbody[@class='b-fight-details__table-body']")

    TOT_COLUMNS = [
            'red_fighter', 'blue_fighter', 'red_knockdowns', 'blue_knockdowns', 'red_sig_strikes_landed', 'red_sig_strikes_att', 
            'blue_sig_strikes_landed','blue_sig_strikes_att', 'red_sig_strikes_pct', 'blue_sig_strikes_pct', 'red_strikes_landed', 
            'red_strikes_att', 'blue_strikes_landed', 'blue_strikes_att', 'red_takedowns_landed', 'red_takedowns_att', 'blue_takedowns_landed',
            'blue_takedowns_att', 'red_takedowns_pct', 'blue_takedowns_pct', 'red_submission_att', 'blue_submission_att',
            'red_reversals', 'blue_reversals', 'red_ctrl_time', 'blue_ctrl_time'
        ]

    SS_COLUMNS = [
            'red_head_strikes_landed', 'red_head_strikes_att', 'blue_head_strikes_landed', 'blue_head_strikes_att', 'red_body_strikes_landed',
            'red_body_strikes_att', 'blue_body_strikes_landed', 'blue_body_strikes_att', 'red_leg_strikes_landed', 'red_leg_strikes_att',
            'blue_leg_strikes_landed', 'blue_leg_strikes_att', 'red_dist_strikes_landed', 'red_dist_strikes_att', 'blue_dist_strikes_landed',
            'blue_dist_strikes_att', 'red_clinch_strikes_landed', 'red_clinch_strikes_att', 'blue_clinch_strikes_landed', 'blue_clinch_strikes_att',
            'red_ground_strikes_landed', 'red_ground_strikes_att', 'blue_ground_strikes_landed', 'blue_ground_strikes_att'
        ]

    tot_data = split_fight_stats(fight_data_[0].text.split('\n'))
    ss_data = split_fight_stats(fight_data_[2].text.split('\n'))

    tot_dict = {col: tot_data[idx] for idx, col in enumerate(TOT_COLUMNS)}
    ss_dict = {col: ss_data[idx + 8] for idx, col in enumerate(SS_COLUMNS)}

    fight_dict = {**tot_dict, **ss_dict}

    return fight_dict