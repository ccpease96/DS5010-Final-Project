**Pythagorean Theorm Use in Baseball**

The purpose of this package is to simulate the expected winning percentage of a baseball lineup on a given night. This program will scrape the web for today's MLB lineups and determine how the team should perform with that specific lineup playing over an entire season.

The code is organized in one file that will pull the lineups with every run. If lineups are to change through the day, running the code will re-pull the data needed to calculated winning percentage.

Functions:
    get_away_lineups()/get_home_lineups(): this function will scrape rotowire.com to pull in Hitting Team, Batting Side, Name
    get_away_pitchers()/get_home_pitchers(): this function will scrape rotowire.com to pull in Pitching Team, Throw Side, Name
    merge(): this function merges away_lineups with home_pitchers and vice versa. Needs to be two valid files so they can be merged on 'Game Number'
    hitting_data(lineup): this adds hitting data to a provided lineup
    final_data(lineup): this finalizes the data by adding the quality of a pitcher and calculating the value of a hitter
    send_groups_to_excel(lineup): this saves lineups to local drive
    calculate_wins(): calculates winning % for team provided by user
    send_lineups_to_excel(lineup): this saves finished lineups to excel
    replace(team): allows you to replace one player in a lineup

Workflow:
    1. Scrape lineup data from rotowire.com
    2. Prompted to see if you want to replace player in select lineup
    3. Calculate wins based on user selected lineup (does not have to be one that was changed)



