import time
import pandas as pd
import numpy as np
import calendar as c

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
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ' '
    while (city not in CITY_DATA):
        #convert all input to lowercase and strip 'city' from input
        city = input("Would you like to see data for Chicago, New York, or Washington?\n").lower().rstrip(' city')

    # get user choice of input - monthly, daily, both or none
    # set variables to 'all' by default
    filter = month = day = 'all' 
    # create list of choices
    list_choice = ['month', 'day', 'both', 'none']
    
    #check for invalid input
    while (filter not in list_choice):
        filter = input("Would you like to filter the data by month, day, both or not at all? Type \"none\" for no time filter\n").lower()
    
    # get user input for month (all, january, february, ... , june) as integer to save space
    # check if month filter is selected and if selected month is in range
    if filter == 'month':
        while (month not in range(1,13)):
            try:
                month = int(input("Which month? Please type your response as an integer (e.g., 1=January).\n"))
            except ValueError:
                continue

    # get user input for day of week (all, monday, tuesday, ... sunday) as integer to save space
    # check if day filter is selected and if valid day is entered
    elif filter == 'day':
        while (day not in range(1,8)):
            try:
                day = int(input("Which day? Please type your response as an integer (e.g., 1=Sunday).\n"))
            except ValueError:
                continue
        
    # get month and day values
    elif filter == 'both':
        # get month and day values
        while (month not in list(range(1,7))):
            try:
                month = int(input("Which month? Please type your response as an integer (e.g., 1=January...6=June).\n"))
            except ValueError:
                continue
        
        while (day not in range(1,8)):
            try:
                day = int(input("Which day? Please type your response as an integer (e.g., 1=Sunday).\n"))
            except ValueError:
                continue


    print('-'*40)
    return city, month, day, filter


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

    # extract month, day of week and hour of day from Start Time to create new columns. Use integers to save space  
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday
    df['hour_of_day'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week']+1 == day]

    return df


def time_stats(df, filter):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month(s)
    #list comprehension returns all the modal values if there is more than one mode and matches to list of months in calendar
    freq_month = [list(c.month_name[1:])[i] for i in df['month'].mode().values]
    print("Most popular month: {}, Count: {}, Filter: {}".format(','.join(freq_month),\
         df['month'].value_counts().max(), filter))

    # display the most common day(s) of week
    #list comprehension returns all the modal values if there is more than one mode and matches to list of months in calendar
    freq_day = [list(c.day_name)[i] for i in df['day_of_week'].mode().values] 
    print("Most popular day: {}, Count: {}, Filter: {}".format(','.join(freq_day), \
        df['day_of_week'].value_counts().max(), filter))

    # display the most common start hour(s)
    freq_hour = ','.join(map(str, (df['hour_of_day'].mode().values))) # remove nparray bracket
    print("Most popular hour: {}, Count:{}, Filter:{}".format(freq_hour, \
        df['hour_of_day'].value_counts().max(), filter))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df, filter):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station(s)
    pop_start = ','.join(list(df['Start Station'].mode().values)) # remove nparray bracket 
    print("Most popular start station: {}, Count: {}, Filter: {}".format(pop_start,\
         df['Start Station'].value_counts().max(), filter))

    # display most commonly used end station
    pop_end = ','.join(list(df['End Station'].mode().values)) # remove nparray bracket
    print("Most popular end station: {}, Count: {}, Filter: {}".format(pop_end,\
         df['End Station'].value_counts().max(), filter))

    # display most frequent combination of start station and end station trip
    end_start = ','.join(list((df['Start Station'] + ',' + df['End Station']).mode().values)) # remove nparray bracket
    print("Most popular start and end station combination: {}, Count: {}, Filter: {}"\
        .format(end_start , df['End Station'].value_counts().max(), filter))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df, filter):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("Total Duration: {}, Count:{}, Filter: {}".format(df['Trip Duration'].sum(),\
         df['Trip Duration'].count(), filter))

    # display mean travel time
    print("Average Duration: {}, Count:{}, Filter:{}".format(df['Trip Duration'].mean(),\
         df['Trip Duration'].count(), filter))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df, filter, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_dict = [str(k) + ': ' + str(v) for k,v in df['User Type'].value_counts().to_dict().items()] #convt. to dict. to fmt. output
    print(*user_type_dict,sep=', ',end=', ')
    print("Filter:",filter)

    # Display counts of gender. Handle exception for absent gender and birth year column in washington.csv
    try:
        gender_dict = [str(k) + ': ' + str(v) for k,v in df['Gender'].value_counts().to_dict().items()]
        print(*gender_dict,sep=', ', end= ', ')
        print("Filter:",filter)
    except KeyError:
        print("No gender column in",CITY_DATA[city]) 

    # Display earliest, most recent, and most common year of birth
    try:
        print("Earliest birth year: {:.0f}, Latest birth year: {:.0f}, Most frequent birth year: {:.0f}"\
        .format(df['Birth Year'].min(), df['Birth Year'].max(), df['Birth Year'].mode()[0]))
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)
    except KeyError:
        print("No year of birth column in",CITY_DATA[city])

def view_data(df):
    """Displays five lines of raw data"""
    ans = ''
    i = 0 
    while (ans != 'no'):
        ans = input("\nDo you want to see first/next five lines of data? Enter 'yes' or 'no'\n").lower()
        if (i < len(df) and ans == 'yes'):
            data_dict = df[i:i+5].to_dict()
            form_data_dict = [str(k) + ': ' + str(v) for k,v in data_dict.items()]
            print(*form_data_dict,sep='\n')
            i += 5
            if (i == len(df)):
                print("End of data!!")
        elif (ans != 'yes' and ans != 'no'):
            continue

def main():

    """while loop continues to call function until user enters No, which breaks the loop and exits the program"""
    while True:
        city, month, day, filter = get_filters()
        df = load_data(city, month, day)

        time_stats(df, filter)
        station_stats(df, filter)
        trip_duration_stats(df, filter)
        user_stats(df, filter, city)
        view_data(df)


        restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
        if restart != 'yes':
            break


if __name__ == "__main__":
	main()
