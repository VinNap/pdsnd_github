import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTH_DATA = ['all', 'january', 'february', 'march', 'april', 'may', 'june']

DAY_DATA = ['all', 'monday', 'tuesday', 'wednesday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!')

    city_name = ''
    while city_name.lower() not in CITY_DATA:
        city_name = input("\nWhich city would you like to analyze? (Please enter either chicago, new york city, washington)\n")
        if city_name.lower() in CITY_DATA:
            city = CITY_DATA[city_name.lower()]
        else:
            print("Sorry, response not recognized. Please enter either chicago, new york city or washington.\n")



    month_name = ''
    while month_name.lower() not in MONTH_DATA:
        month_name = input("\nWhich month would you like to filter the data by? (Please enter either 'all' to apply no month filter or enter january, february, march, april, or june)\n")
        if month_name.lower() in MONTH_DATA:
            month = month_name.lower()
        else:
            print("Sorry, response not recognized. Please enter either 'all' to apply no month filter or january, february, march, april, may, or june.\n")



    day_name = ''
    while day_name.lower() not in DAY_DATA:
        day_name = input("\nWhich day would you like to filter the data by? (Please enter either 'all' to apply no day filter or enter monday, tuesday, wednesday, thursday, friday, saturday, or sunday)\n")
        if day_name.lower() in DAY_DATA:
            day = day_name.lower()
        else:
            print("Sorry, response not recognized. Please enter either 'all' to apply no day filter or monday, tuesday, ... sunday.\n")

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
    df = pd.read_csv(city)

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    if month != 'all':
        month = MONTH_DATA.index(month)
        df = df.loc[df['month'] == month]

    if day != 'all':
        df = df.loc[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    common_month = df['month'].mode()[0]
    print('The most common month is: ', common_month)

    common_day = df['day_of_week'].mode()[0]
    print('The most common day of the week is: ', common_day)

    common_hour = df['hour'].mode()[0]
    print('The most common start hour of the day is: ', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    common_start_station = df['Start Station'].mode()[0]
    print('The most common start station is: ', common_start_station)

    common_end_station = df['End Station'].mode()[0]
    print('The most common end station is: ', common_end_station)

    frequent_combo = (df['Start Station'] + "||" + df['End Station']).mode()[0]
    print("The most frequent combination of start station and end station trip is : " + str(frequent_combo.split("||")))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_travel_time = df['Trip Duration'].sum()
    print('The total travel time is: ', total_travel_time)

    mean_travel_time = df['Trip Duration'].mean()
    print('The mean travel time is: ', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_types = df['User Type'].value_counts()
    print("The count of the different user types are: {} \n".format(user_types))

    if city != 'washington.csv':
        print('Gender Counts: ',df['Gender'].value_counts())

        earliest_year = df['Birth Year'].min()
        print('The earliest year of birth is: ', earliest_year)
        recent_year = df['Birth Year'].max()
        print('The most recent year of birth is: ', recent_year)
        common_year = df['Birth Year'].mode()[0]
        print('The most common year of birth is: ', common_year)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    """Displays raw data on user request.
    Args:
        (DataFrame) df - Pandas DataFrame containing city data filtered by month and day
    """
    print(df.head())
    next = 0
    while True:
        view_raw_data = input('\nWould you like to view the next five rows of raw data? (Please enter yes or no)\n')
        if view_raw_data.lower() != 'yes':
            return
        next = next + 5
        print(df.iloc[next:next+5])

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        while True:
            view_raw_data = input('\nWould you like to view the first five rows of raw data? (Please enter yes or no)\n')
            if view_raw_data.lower() != 'yes':
                break
            display_raw_data(df)
            break

        restart = input('\nWould you like to restart? (Please enter yes or no)\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
