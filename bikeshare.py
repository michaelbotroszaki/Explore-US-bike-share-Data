import time
import pandas as pd


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    
    city = ""
    month = ""
    day = ""
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # Getting user input for city (chicago, new york city, washington)
    
    while city not in CITY_DATA  :       
        city=input("Would you like to see data for chicago, new york, or washington?\n").lower()
        if city not in CITY_DATA:
            print("please enter one of the below cities:- \n chicago \n new york \n washington \n")
            
    # Getting user input for month (all, january, february, ... , june)
    months=['january','february','march','april','may','june','all'] # month list to be the base of month name searching input 
    
    while month not in months:
        month=input("which month would you like to filter type month name ex:'january','february',...etc \n or type 'all' for no filter\n").lower()
        if month not in months:
            print("please enter one of the below months:-\n'january','february','march','april','may','june'.\n")
    # Getting user input for day of week (all, monday, tuesday, ... sunday)
    weekday=['monday','tuesday','wednesday','thursday','friday','saturday','sunday','all'] # weekday list to be the base of day name searching input 
    
    while day not in weekday:
        day=input("which day would you like to filter type day name ex:'monday','tuesday',...etc \n or type 'all' for no filter\n").lower()
        if day not in weekday:
            print("please enter one of the below days:-\n'monday','tuesday','wednesday','thursday','friday','saturday','sunday'.\n")
                       
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
    df=pd.read_csv(CITY_DATA[city])
    
    """remove rows tha have NAN values in dataframe """
    df.dropna(0,inplace=True)
    """convert start time column to datetime"""
    df['Start Time']=pd.to_datetime(df['Start Time'])
    
    """extract month column from start time column and convert it to its relevant month name"""
    df['month']=df['Start Time'].dt.month_name()  
    
    """extract day column from start time column and convert it to its relevant day name"""
    df['day_of_week']=df['Start Time'].dt.day_name() 
    
    """extract hour column from start time column"""
    df['hour']=df['Start Time'].dt.hour       
    
    """filter by month to create new dataframe based on user choice"""
    if month != 'all':
        df=df[df['month']==month.title()]
        
    """filter by day to create new dataframe based on user choice"""
    if day != 'all':
        df=df[df['day_of_week']==day.title()]   
    
           
    return df


def time_stats(df,month,day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month based on user choice
    if month =='all':
        print("Most common month: ",df['month'].mode()[0])
    
    # Display the most common day of week based on user choice
    if day =='all':
        print("Most common day of week: ",df['day_of_week'].mode()[0])

    # Display the most common start hour
    p=df['hour'].mode()[0]
    
    """if condition to print time based on 12 hour system"""
    if p>12:
        p-=12
        print("most common start hour: ",p," pm")
    elif p<12:
        print("most common start hour: ",p," am")
    else:
        print("most common start hour: ",p," pm")
        

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    print("\n Most commonly used Start Station: ",(df['Start Station'].mode()[0]))

    # Display most commonly used end station
    print("\n Most commonly used End Station: ",(df['End Station'].mode()[0]))

    # Display most frequent combination of start station and end station trip
    print("\n Most frequent combination of start station and end station trip: ",((df['Start Station']+ " - " +df['End Station']).mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    
    """Getting statistics on the total and average trip duration."""
    Trip_Duration_sum=df['Trip Duration'].sum()
    Trip_Duration_mean=df['Trip Duration'].mean()
    
    """Trip_Duration function main job is that converting the total and average trip duration from seconds to hours and minutes and display it depending on its value
    x----> the value that will be converted 
    y----> the text that will be printed based evey case 
    """
    def Trip_Duration (x,y):
        h=x//3600
        h1=x%3600
        m=h1//60
        s=h1%60
        
        if h>1 and m>1 and s>1:
            print(y,h," hours",m," minutes",s," seconds" )
        elif h>1 and s>1 and m <1 :
            print(y,h," hours",m," minute",s," seconds" )    
        elif h>1 and s<1 and m <1:
            print(y,h," hours",m," minute",s," second" )
        elif h<1 and m>1 and s>1 :          
            print(y,h," hour",m," minutes",s," seconds" )
        elif h<1 and m<1 and s>1:
            print(y,h," hour",m," minute",s," seconds" )    
        else:
            print(y,h," hour",m," minute",s," second" )
            
    
    # Display total travel time 
    Trip_Duration (Trip_Duration_sum,"Total travel time: ")
    # Display mean travel time
    Trip_Duration (Trip_Duration_mean,"Average travel time: ")
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(city,df):
    """Displays statistics on bikeshare users """

    print('\n Calculating User Stats...\n')
    start_time = time.time()

    
    if city !='washington':
        # Display earliest, most recent, and most common year of birth 
        print("\n Earliest year of birth :",int(df['Birth Year'].max()))
        print("\n Most recent year of birth :",int(df['Birth Year'].min()))
        print("\n Most common year of birth :",int(df['Birth Year'].mode()[0]))
        
        # Display counts of gender
        print("\n Gender: ",(df['Gender'].value_counts()))

    
    # Display counts of user types
    print("\n user types: ",(df['User Type'].value_counts()))    

   # infinite while loop to make sure that user ALWAYS write the right yes or no and displayes raw data until user type no or until reaching the end of dataframe's data  
    z=['yes','no']
    n=5
    while True:
        print("\n",df.head(n))
        i=input("\n Would you like to View more individual trip data? Enter yes or no \n").lower()
        n+=5
        while i not in z :
            i=input("\n False Attempt!!!,Please Enter yes or no \n").lower()            
        if i != 'yes'and i in z:
            break
        elif i=='yes' and n==df.shape[0]:
            print("\n",df.head(n))
            print("\n we have reached the last of our data!!!!!! \n")
            break
       
            
    print("\n This took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df,month,day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(city,df)
       # infinite while loop to make sure that user ALWAYS write the right yes or no in order to restart the program  
        l=['yes','no']
        restart = input('\n Would you like to restart? Enter yes or no.\n')
        
        while restart.lower() not in l:
            restart =  input("\n False Attempt!!!,Please Enter yes or no \n")
        if  restart.lower() != 'yes' and restart in l :
            break
        

if __name__ == "__main__":
	main()
