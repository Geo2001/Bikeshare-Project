#Professional track project 1 

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
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Please enter city name from one of the cities : chicago, washington, new york city:").lower()
    
    while city not in CITY_DATA:
        city = input("Please enter city name from one of the cities : chicago, washington, new york city:").lower()

    # get user input for month (all, january, february, ... , june)
    valid_months = ['all','january','february','march', 'april', 'may', 'june']
    month = input("Please enter your desired month or 'all' for all months:").lower()
    
    while month not in valid_months:
        month = input("Please enter a valid month from :{} ".format(valid_months)).lower() 
        
    

    # get user input for day of week (all, monday, tuesday, ... sunday)
    valid_days = ['all','sunday','monday','tuesday','wednesday','thursday','friday','saturday']
    day = input("Please enter weekday or 'all' for all days:").lower()
    while day not in valid_days:
        day = input("Please enter a valid weekday from :{} ".format(valid_days)).lower()
       
    



    #Note that we lowercased city,day,month for later purposes of use in following functions

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

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name 

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    df['Start Time'] = pd.to_datetime(df['Start Time']) #repeated here in case of calling this function on a ready df directly without using load_data(df)
    Month_Strings = {1 : 'January', 2 : 'February', 3 : 'March',
                  4 : 'April', 5 : 'May', 6 : 'June'}


    # TO DO: display the most common month
    df['month'] = df['Start Time'].dt.month
    print('The most common month of travel is: {}'.format(Month_Strings[df['month'].mode()[0]]))
    #we can make it print months names with datetime_object = datetime.datetime.strptime(month_number, "%m")


    # TO DO: display the most common day of week
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    print('The most day of week for travel is: {}'.format(df['day_of_week'].mode()[0]))


    # TO DO: display the most common start hour
    df['hour']= df['Start Time'].dt.hour
    print('The most common hour of start of travel is: {}'.format(df['hour'].mode()[0]))




    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print("The most common start station is :{} ".format(df['Start Station'].mode()[0]))



    # TO DO: display most commonly used end station
    print("The most common end station is :{}".format(df['End Station'].mode()[0]))


    # TO DO: display most frequent combination of start station and end station trip
    df['route'] = df['Start Station'] + " to " + df['End Station']
    print("The most common start-end station combination is :{}".format(df['route'].mode()[0]))



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    df['duration'] = pd.to_datetime(df['End Time']) - pd.to_datetime(df['Start Time'])


    # TO DO: display total travel time
    print("The total time of travel for all trips is: {}".format(df['duration'].sum())) #Summation of all trips for all routes

    # TO DO: display mean travel time
    mean = df['duration'].mean() 
    print("The average time for a trip is: {} minutes and {} seconds".format(mean.components.minutes,mean.components.seconds))  #Displaying duration in just minutes and seconds as it never exceeds an hour for all given csv files


    


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of gender

    if city != 'washington':                         #Because the following two columns arent included in washington.csv
        # TO DO: Display earliest, most recent, and most common year of birth
   
        print("The oldest user was born at: {} \n".format(int(min(df['Birth Year']))))   #earliest birth year means oldest user
    
        print("The youngest user was born at: {} \n".format(int(max(df['Birth Year']))))  
        print("The most common year of birth among users is: {} \n".format(int(df['Birth Year'].mode()[0])))
        print("The number of users for each gender is displayed as follows: \n")
        print(df['Gender'].value_counts().to_frame())    #to_frame() removes the datatypes at the bottom of the query for smoother output to the user
        print("\n")
        

    # TO DO: Display counts of user types
    print("The numbers of each type of users are displayed as follows: \n")
    print( df['User Type'].value_counts().to_frame())  
    print("\n")

    
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def display_raw_data(df):
    '''Displays 5 rows of raw data upon request from the user
       
       args: filtered DataFrame
            
     '''
    # given that df is send as arg after calling load_data therefore the user already applied the desired filters and we filtered it
    df.drop(['Unnamed: 0','month', 'day_of_week', 'hour', 'route','duration'], inplace = True, axis = 1) #Remove the helper cols that we used as helpers in functions, as they're undesired for user display
    i=0
    for i in range(df.size-5):      #to be ready to print the whole df in successive rows of 5 , we here ignored the case where there're rows less than 5 as the user specified them to be in rows of 5

        try :
            print(df.iloc[i:i+5])
        except IndexError:
            print("we are done with displaying the available data in rows of 5, \n Thank You for your time!!")
            break


        i += 5
        proceed = input("Do you like to see 5 more rows, Please type 'yes' or 'no' only: ").lower()
        
        while proceed != 'yes' and proceed != 'no':
            proceed = input("Do you like to see 5 more rows, Please type 'yes' or 'no' only: ").lower()
            
        if proceed == 'no':
            break
    '''if proceed == 'yes' & i< df.size-1 :
        print(df.iloc[i:df.size-1])''' #Just uncomment these two lines if we are interested in displaying the very last batch of data even if they wont be enough to compose a 5 rows block
    print("we are done with displaying the available data in rows of 5, \n Thank You for your time!!")
          



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
        if restart != 'yes':
            break


if __name__ == "__main__":
	main()
   

