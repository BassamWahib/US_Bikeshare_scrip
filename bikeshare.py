import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    cities = ['chicago', 'new york city', 'washington']
    while True:
        try:
            city = str(input('Which city you would like to analyze\nChicago, New York City or Washington: ')).lower()
            if city in cities:
                break
            elif city not in cities:
                print('OOOOPS! Wrong entry.\nPlease enter either: chicago, New York City or Washington')
        except:
            print('I don\'t understand your choice')  
        
    # TO DO: get user input for month (all, january, february, ... , june)
    month_range = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    while True:
        try:
            month = str(input('Enter the required month name or all: ')).lower()
            if month in month_range:
                break
            elif  month not in month_range:
                print('OOOOPS! Wrong entry.\nPlease enter either: january, february, march, april, may, june or all')
        except:
            print('I don\'t understand your choice')
    
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    while True:
        try:
            day = str(input('Enter the required weekday or all: ')).lower()
            if day in days:
                break
            elif day not in days:
                print('OOOOPS! Wrong entry.\nPlease enter either: monday, tuesday, wednesday, thursday, friday, saturday, sunday or all')
        except:
            print('I don\'t understand your choice')     

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
    # load data file in a dataframe
    df = pd.read_csv(CITY_DATA[city])
    # convert start time column to date and time format
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month number to new column
    df['month'] = df['Start Time'].dt.month
    # extract weeday name to new column
    # I used .day_name() which I found on nfpdiscussions instead of the non-working .weekday_name
    df['weekday'] = df['Start Time'].dt.day_name()
    # filter by month
    if month != 'all':
        months =['january','february','march','april','may','june']
        month = months.index(month)+1
        df = df[df['month'] == month]    
    # filter by weekday name
    if day != 'all':
        df = df[df['weekday'] == day.title()]
                     
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    months =['january','february','march','april','may','june']
    # To get the month name instead of month number
    popular_month = months[df['month'].mode()[0] - 1].title()
    print('The most popular month: ', popular_month)
    # TO DO: display the most common day of week
    popular_day = df['weekday'].mode()[0]
    print('The most popular day of week: ', popular_day)
    # TO DO: display the most common start hour
    df['Hour'] = df['Start Time'].dt.hour
    popular_hour = df['Hour'].mode()[0]
    print('The most popular hour: ', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station= df['Start Station'].mode()[0]
    print('The most popular start station: ', popular_start_station)
    # TO DO: display most commonly used end station
    popular_end_station= df['End Station'].mode()[0]
    print('The most popular end station: ', popular_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    df['Trip'] = df['Start Station'] + ' to '+ df['End Station']
    popular_trip = df['Trip'].mode()[0]
    print('The most popular trip: from ', popular_trip)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_trip_duration = df['Trip Duration'].sum()

    # TO DO: display mean travel time
    average_trip_duration = df['Trip Duration'].mean()
    print('Total duration: ', total_trip_duration, ' & Average duration: ', average_trip_duration)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_type_count = df['User Type'].value_counts()
    print('The user type count:\n', user_type_count)
    # TO DO: Display counts of gender
    try:
        gender_count = df['Gender'].value_counts()
        print('\nThe gender count:\n', gender_count)
    # To avoid error in case of data absence in washington
    except:
        print('\nNo gender data to share')
    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        # I used .sort_values() from stackoverflow
        earliest_year = int(df['Birth Year'].sort_values(ascending = True).iloc[0])
        most_recent_year = int(df['Birth Year'].sort_values(ascending = False).iloc[0])
        most_common_year = int(df['Birth Year'].mode()[0])
        print('\nYear of birth statistics:\nEarliest:', earliest_year, '\nMost recent:', most_recent_year, '\nMost common:', most_common_year)
    # To avoid error in case of data absence in washington
    except:
        print('\nNo birth year data to share')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    
def data_lines(df):
    """Displays raw data lines five by five upon user's request."""
    i = 0
    user_acceptance = input('Do you like to see first five data lines? Please type Yes or No: ').lower()
    while True:
        if user_acceptance != 'yes':
            print('Thanks for using my script')  
            break
        print(df.iloc[i:i+5])        
        user_acceptance = input('Do you like to see the next five data lines? Please type Yes or No: ').lower()
        # To loop the next five indices
        i += 5
                
            

       
    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        data_lines(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
