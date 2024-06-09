# WingsOnWheels (How to implement a code project):

## Step 1: Clone the Repository.

1.	Go to the GitHub page of the repository you want to clone.
2.	Click the "Code" button and copy the URL provided
3.	Open Terminal and Navigate to the Desired Directory. (example; cd path/to/your/directory)
4.	Clone by enter copy the URL on Terminal  (git clone https://github.com/nabSwin99/WingsOnWheels.git)
5.	After completing, it should be as figure1
   
	![image](https://github.com/nabSwin99/WingsOnWheels/assets/146166502/e591cfab-924e-49b4-b41d-01a6fdc4a7d9)
<p align="center">Figure 1</p>

6. 	Use the cd command to navigate to the directory cloned repository.

7. 	Open Visual Studio to view source code.

#### *Note: All the libraries and dependencies will be pulled along with the code source, so you may not need to install them seperately. Below are instrustions just in case if the dependencies didn't work properly.

Dependencies Installing Instructions:
1. Create a "requirements.txt" file and include all the below text for dependencies:

	Django>=3.2,<4.0

	osmnx>=1.1

	networkx>=2.5

	folium>=0.12.1

	geopy>=2.2.0


2. After that run the command "pip install -r requirements.txt" on the terminal of the current project directory.


## Step 2: Connect project with database.

1. 	Install PostgreSQL
2.	Install pgAdmin
3.	Open pgAdmin and create database name WingsOnMeals as shown in figure 2. right-click on "Database and select "Create" -> "Database”.
   
	![image](https://github.com/nabSwin99/WingsOnWheels/assets/146166502/b4883aa8-3bf5-4d04-8fe5-b1fd200c2bec)

<p align="center">Figure 2</p>

4. 	In Visual Studio, navigate to setting.py which is under WingsOnWheels and move to database configurations like figure 3. The password should be changed following the created password during pgAdmin installation.
  
   ![image](https://github.com/nabSwin99/WingsOnWheels/assets/146166502/e182a45e-3b2a-4b50-b3dc-5ef3b6122c69)

<p align="center">Figure 3</p>

5. 	Open terminal in visual studio and enter "python manage.py migrate" in command. Then, the tables and their relationships will be created in the database using Django migrations.

6. 	Then ensure your current directory is of the project (example: "WingsOnWheels").

7. 	Run the project on the local server by entering the command "python manage.py runserver". Then, the url link to access web application is displayed as shown in figure 4.

   ![image](https://github.com/nabSwin99/WingsOnWheels/assets/146166502/e2707351-2ad3-43fc-a25f-ccfede8c06ca)

   <p align="center">Figure 4</p>

8. 	Navigate to "http://127.0.0.1:8000" to access web application.

 	
## Step 3: How to add food items to database.

#### *Note: The database won't have any records or data regarding store items so it needs to be manually added using pgAdmin.

1. Open pgAdmin and navigate to WingsOnWheels > Schemas > Tables > playground_menuitem. Right-click on playground_menuitem and select "View/Edit Data" -> "All Rows" as shown in figure 5.

![image](https://github.com/nabSwin99/WingsOnWheels/assets/146166502/48829932-fdee-48d8-88ef-a42ea0088e45)

  <p align="center">Figure 5</p>

2. Click add row as shown in figure 6.
   
![image](https://github.com/nabSwin99/WingsOnWheels/assets/146166502/aa7d5f65-ae62-4ae9-907e-e70f84a18ffd)

  <p align="center">Figure 6</p>

3. In figure7, add the data in each column and Then click save data change. The menu item will be save to database.  

![image](https://github.com/nabSwin99/WingsOnWheels/assets/146166502/9045849b-a67a-4c71-9c0c-7175f98fae58)

  <p align="center">Figure 7</p>


