import pandas as pd 
import datetime
import time

city_dict = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' }
mth_list = ['January', 'February', 'March', 'April', 'May', 'June', 'All']
dow_list = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday','Saturday', 'Sunday', 'All']
yes_list = ['Yes', 'Y', 'Ya', 'Ye', 'Yeah', 'Yup', 'Yea']


def get_city():
    """
    Asks user to specify a city to analyze.

    Returns:
        (str) name of the city to analyze
    """

    city_input = input('\nPlease choose a city (%s) to explore:\n' % ', '.join(city_dict))
    while not city_dict.get(city_input.title()):
        city_input = input('\nPlease enter a correct city name from the following:\n%s\n' \
                           % ', '.join(city_dict))
    return city_input.title()


def load_df(file_name):
    """
    Loads data for the specified city.

    Args:
        (str) file_name - name of the file containing city data
    Returns:
        (DataFrame) unfiltered Pandas DataFrame containing city data
    """

    df = pd.read_csv(file_name)
    df.pop('Unnamed: 0')
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month_name(locale = 'English')
    df['dow'] = df['Start Time'].dt.day_name(locale = 'English')
    df['hour'] = df['Start Time'].dt.hour
    df['trip'] = df['Start Station'] + ' ~ ' + df['End Station']
    return df


def get_filters():
    """
    Asks user to specify a month and/or a day of the week to analyze.

    Returns:
        (str) name of the month to filter by, or "All" to apply no month filter
        (str) name of the day of week to filter by, or "All" to apply no day filter
    """

    mth_input = input('\nWhich month (%s) would you like to investigate in details? \
                      \nPlease enter "All" if no month filtering is needed\n' % ', '.join(mth_list[:-1]))
    while mth_input.title() not in mth_list:
        mth_input = input('\nPlease enter a correct month from the following: \
                          \n%s, or enter "All" for no filtering \n' % ', '.join(mth_list[:-1]))
    mth_input = mth_input.title()

    dow_input = input('\nWhich day of the week (%s) would you like to investigate in details? \
                      \nPlease enter "All" if no day of the week filtering is needed\n' % ', '.join(dow_list[:-1]))
    while dow_input.title() not in dow_list:
        dow_input = input('\nPlease enter a correct day of the week from the following: \
                          \n%s, or enter "All" for no filtering \n' % ', '.join(dow_list[:-1]))
    dow_input = dow_input.title()
    return mth_input, dow_input


def create_sub_df(df, mth, dow):
    """
    Creates sub DataFrame filtered by month (if any) and day (if any)

    Args:
        (DataFrame) df - unfiltered Pandas DataFrame containing city data
        (str) mth - name of the month to filter by, or "All" to apply no month filter
        (str) dow - name of the day of week to filter by, or "All" to apply no day filter
    Returns:
        (DataFrame) filtered Pandas DataFrame containing city data
    """

    if mth == 'All' and dow == 'All':
        return df
    else:
        query_str = ('' if mth == 'All' else 'month == @mth') \
                    + (' & ' if mth != 'All' and dow != 'All' else '') \
                    + ('' if dow == 'All' else 'dow == @dow')
        return df.query(query_str)
    

def explore_data(df):
    """
    Explore data of one specified city with filtered month, and/or day of the week.

    Args:
        (DataFrame) unfiltered Pandas DataFrame containing city data
    """

    mth_input, dow_input = get_filters()
    sub_df = create_sub_df(df, mth_input, dow_input)
    display_stats(sub_df, mth_input, dow_input)
    display_raw_data = input('Would you like to see the first 5 lines of the original data? \
                             \nPlease enter "Yes" or "No"\n')
    if display_raw_data.title() in yes_list:
        print('\n')
        print(sub_df.head())


def display_stats(df, mth, dow):
    """
    Displays statistics on the most frequent times of travel, 
    the most popular stations and trip, the total and average trip duration
    and statistics relating to bikeshare users.
    """

    start_time = time.time()
    print('\n' + '-'*40)

    if mth == 'All':
        print('\nThe most popular month for travel%s is: %s' \
              % (show_mth_dow(mth, dow), df.month.mode()[0])) 
    if dow == 'All':
        print('\nThe most popular day of the week for travel%s is: %s' \
              % (show_mth_dow(mth, dow), df.dow.mode()[0]))
    print('\nThe most popular hour for travel%s is: %d:00 ~ %d:00' \
          % (show_mth_dow(mth, dow), df.hour.mode()[0], df.hour.mode()[0] + 1))
    print('\nThe most popular start station%s is: %s' \
          % (show_mth_dow(mth, dow), df['Start Station'].mode()[0]))
    print('\nThe most popular end station%s is: %s' \
          % (show_mth_dow(mth, dow), df['End Station'].mode()[0]))
    print('\nThe most popular trip%s is: %s' \
          % (show_mth_dow(mth, dow), df.trip.mode()[0]))
    print('\nThe total travel time%s is: %s' \
          % (show_mth_dow(mth, dow), convert_time(df['Trip Duration'].sum())))
    print('\nThe average travel time%s is: %s' \
          % (show_mth_dow(mth, dow), convert_time(df['Trip Duration'].mean())))
    print('\nTotal number of users in each user type%s are as follow:\n%s' \
          % (show_mth_dow(mth, dow), df['User Type'].value_counts().to_string()))

    try:
        print('\nTotal number of users in each gender group%s are as follow:\n%s' \
              % (show_mth_dow(mth, dow), df['Gender'].value_counts().to_string()))
        print('\nThe most common birth year of users%s is %d, with the oldest user born in %d and the youngest born in %d\n' \
              % (show_mth_dow(mth, dow), int(df['Birth Year'].mode()[0]), int(df['Birth Year'].min()), int(df['Birth Year'].max())))
    except:
        print('\nUnfortunately no further user related data is available for Washington\n')
    
    print('\nThis took %s seconds.' % round(time.time() - start_time, 4))
    print('-'*40)


def convert_time(time):
    """
    Makes time durtion into a more reader friendly format than in total number of seconds for display,
    which further transfers timedelta's way of displaying in "HH:MM:SS" into "HH hour(s), MM minute(s), SS second(s)".

    Args:
        (float or int) time - time duration in seconds
    Returns:
        (str) time during displayed in "DD days, HH hour(s), MM minute(s), SS second(s)"
    """
    
    t_str = str(datetime.timedelta(seconds=int(time))).split(':')
    t_units = [' hour(s)', ' minute(s)', ' second(s)']
    t_msg = [str(int(ts[-2:])) + tu for ts, tu in zip(t_str, t_units) if int(ts[-2:]) != 0]
    return ('%s %s' % (t_str[0][:-2].strip(), ', '.join(t_msg))).strip()


def show_mth_dow(mth, dow):
    """
    Display the month (if any) and day of the week (if any) filter(s) in the messages displaying relevant statistics.
    """

    return ('' if dow == 'All' else ' on ' + dow + 's') + ('' if mth == 'All' else ' in ' + mth )


def main():

    city_input = get_city()
    df = load_df(city_dict[city_input])
    continue_mth_dow = 'Yes'
    while continue_mth_dow.title() in yes_list:
        explore_data(df)
        continue_mth_dow = input('\nWould you like to explore ' + city_input + ' in a different way? \
                                 \nPlease enter "Yes" or "No"\n')


print('Hi there, let\'s explore some US bikeshare data (*^__^*)')
continue_cities = 'Yes'
while continue_cities.title() in yes_list:
    main()
    continue_cities = input('\nWould you like to explore another city? \
                             \nPlease enter "Yes" or "No"\n')