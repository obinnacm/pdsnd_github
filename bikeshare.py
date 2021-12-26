import time
import datetime as dt
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

CALENDAR_MONTH = ['all','january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']


WEEK_DAY = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


def isValidCity(cityName):
    """Check that user's city input is valid"""
    city_list = []
    for key in CITY_DATA:
        city_list.append(key)
    if cityName not in city_list:
        return False
    return True

def getCity():
    """Get user's city input"""
    while True:
        print('Enter name of city to analyze. Valid cities are Chicago, New York City and Washington.')
        city_to_analyze = str(input(">>> ")).strip().lower()
        if not isValidCity(city_to_analyze):
            continue
        else:
            break
    return city_to_analyze


def isValidMonth(monthName):
    """Check that user's month input is valid"""
    if monthName not in CALENDAR_MONTH:
        return False
    return True


def getMonth():
    """Get user's month input"""
    while True:
        print('Filter for the calendar month to analyze.\n You can enter All for all months or any of the twelve calendar months.\nHowever data is available for January, February, March, April, May, June')
        month_to_analyze = str(input(">>> ")).strip().lower()
        if not isValidMonth(month_to_analyze):
            continue
        else:
            break
    return month_to_analyze


def isValidDay(dayName):
    """Check that user's day input is valid"""
    if dayName not in WEEK_DAY:
        return False
    return True


def getDay():
    """Get user's day input"""
    while True:
        print('Filter for the week day to analyze. \nEnter All for all days or any of Monday, Tuesday, wednesday, Thursday, Friday, Saturday, or Sunday.')
        day_to_analyze = str(input(">>> ")).strip().lower()
        if not isValidDay(day_to_analyze):
            continue
        else:
            break
    return day_to_analyze


def isValidYesOrNo(yesOrNoresponse):
    """Validate yes or no answer values"""
    yesOrNoResponse_list = ['yes','y','no','n']
    if yesOrNoresponse not in yesOrNoResponse_list:
        return False
    return True


def getResponse():
    """Get a yes or no response from user"""
    while True:
        print('Enter y or yes to accept and n or no to decline.')
        yesOrNoresponse = str(input(">>> ")).strip().lower()
        if not isValidYesOrNo(yesOrNoresponse):
            continue
        else:
            break
    return yesOrNoresponse


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = getCity()

    # get user input for month (all, january, february, ... , june)
    month = getMonth()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = getDay()

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month from Start Time as month name
    df['month'] = pd.DatetimeIndex(df['Start Time']).month_name()

    # extract day from Start Time as day name
    df['day_of_week'] = pd.DatetimeIndex(df['Start Time']).day_name()

    # filter by month if applicable
    if month != 'all':
        df = df[df['month'] == month.title()]
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]

    print('Most common month:', common_month)

    # display the most common day of week
    common_day_of_week = df['day_of_week'].mode()[0]

    print('Most common day of week:', common_day_of_week)

    # display the most common start hour

    df['hour'] = pd.DatetimeIndex(df['Start Time']).hour

    common_start_hour = df['hour'].mode()[0]

    print('Most common Start Hour:', common_start_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    try:
        common_start_station = df['Start Station'].mode()[0]
        print('Most common Start Station:', common_start_station)
    except KeyError as err:
        print('\nOops! Calculations involving {} failed because your current city data does not have {} column.'.format(err,err))

    try:
        common_end_station = df['End Station'].mode()[0]
        print('Most common Start end:', common_end_station)

        df['Start_and_End'] = df['Start Station'] + ' ==> ' + df['End Station']
        freq_start_and_end_station = df['Start_and_End'].mode()[0]
        print('Most frequent Start and end Station trip:', freq_start_and_end_station)
    except KeyError as err:
        print('\nOops! Calculations involving {} failed because your current city data does not have {} column.'.format(err,err))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    try:
        total_travel_time = dt.timedelta(seconds=int(df['Trip Duration'].sum()))
        print('Total travel time:', total_travel_time)

        mean_travel_time = dt.timedelta(seconds=int(df['Trip Duration'].mean()))
        print('Average travel time:', mean_travel_time)
    except KeyError as err:
        print('\nOops! Calculations involving {} failed because your current city data does not have {} column.'.format(err,err))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        print('\nYour Current filters: CITY == {}, MONTH == {}, and DAY == {}'.format(city.title(),month.title(),day.title()))
        print('='*100)
        df = load_data(city, month, day)
        if df.empty:
            print('The program has restarted automatically because there is no data returned for the month of {} or {} in {}. Data is available from January to June.'.format(month.title(),day.title(),month.title()))
            continue
        else:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)          
        print('\n****Would you like to restart?*****')
        restart = getResponse()
        if restart == 'yes' or restart == 'y':
            continue
        else:
            break

if __name__ == "__main__":
	main()
