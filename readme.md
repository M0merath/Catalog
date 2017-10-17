# Gastronaut.com: my Udacity catalog project

## What is this?
Gastronaut.com is a website for foodies that catalogs recipes by category. Any user can view the recipes, but only an authenticated user can create, edit, or delete recipes; and only if they are the author.

## Files included
* catalog.py - the main Python executeable
* client_secrets.json - needed to authenticate with Google+
* fb_client_secrets.josn - needed to authenticate with Facebook
* database_setup.py - used to recreate the gastronaut.db database
* gastronaut.db - the database, containing all category, recipe, and user data
* README.md - this instruction file you're reading now
* styles.css (in the static folder) - defines the visual style of gastronaut.com
* HTML files (in the templates folder) - these define the web links of gastronaut.com

## How do I use this?
1. Download all files to a directory on your hard drive. If downloading from Github, you will need to "clone" or "fork" the repository. Instructions can be found on github.com.
2. Run Git Bash. Navigate to your Vagrant directory and type "vagrant up". When finished, type "vagrant ssh". Navigate to the vagrant directory in your virtual machine, and then "cd catalog" to reach the catalog project.
3. To start the (local) web site for this project, type "python catalog.py". If successful, information related to the debugger and "http://localhost:8000" should appear.
4. Using any web browser, set your address to "http://localhost:8000". This is the main page for the project.
5. The web site "gastronaut.com" should appear! Navigation by way of hyperlinks should be self-explanatory. However, you will not be able to create/add/delete categories and/or recipes unless you click the "Login" link at the top of the page. You must have a Facebook or Google+ account to log in. You may not edit nor delete anything you did not create with that same account!
6. To extract JSON data from this website, navigate to "http://localhost:8000/category/JSON" for a JSON of the food categories. Or "http://localhost:8000/category/category_#/recipe/recipe_#/JSON" for an individual recipe. You must supply the correct category and recipe numbers for that item. For example: "http://localhost:8000/category/1/recipe/2/JSON" displays the JSON for a "Sidecar". 
