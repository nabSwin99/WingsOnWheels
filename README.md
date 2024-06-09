# WingsOnWheels
How to implement a code project
Clone the Repository.
1.	Go to the GitHub page of the repository you want to clone.
2.	Click the "Code" button and copy the URL provided
3.	Open Terminal and Navigate to the Desired Directory.
cd path/to/your/directory
4.	Clone by enter copy the URL on Terminal
git clone https://github.com/nabSwin99/WingsOnWheels.git
5.	Use the cd command to navigate to the directory cloned repository.
Enter in Terminal cd WingsOnWheels 

6.	Open Visual Studio to view source code
Enter in Terminal code ..
	Connect project with database.
	Install database
1.	Install PostgreSQL
2.	Install pgAdmin
3.	Open pgAdmin and create database name WingsOnMeals as shown in figure2. right-click on "Database and select "Create" -> "Database”
4.	In Visual Studio, navigate to setting.py which is under WingsOnWheels  and move to database like figure3. The password should be changed following the created password during pgAdmin installation.
5.	Open terminal in visual studio and enter
 python manage.py migrate in command. Then, the database will be connected to pgAdmin4.
6.	You can check in pgAdmin4 by navigating to WingsOnMeals > Schemas > Tables, where you can see the tables.
7.	Ensure your current directory is WingsOnWheels by enter command in Terminal 
cd WingsOnWheels 
8.	Run the Development Server on terminal in Visual Studio by command entering
python manage.py runserver 
Then, the url link to access web application is displayed.
9.	Navigate to http://127.0.0.1:8000 to access web application.
How to add food items to database.
10. Open pgAdmin and navigate to WingsOnWheels > Schemas > Tables > playground_menuitem. Right-click on playground_menuitem and select "View/Edit Data" -> "All Rows".
11. click Add row
12. Add the data in each column and Then click save data change. The menu item will be save to database.
 
