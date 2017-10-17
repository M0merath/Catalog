How to use this catalog project:

1. Download all files to a directory on your hard drive. If downloading from Github, you will need to "clone" or "fork" the repository. Instructions can be found on github.com.
2. Run Git Bash. Navigate to your Vagrant directory and type "vagrant up". When finished, type "vagrant ssh". Navigate to the vagrant directory in your virtual machine, and then "cd catalog" to reach the catalog project.
3. To start the (local) web site for this project, type "python catalog.py". If successful, information related to the debugger and "localhost:8000" should appear.
4. Using any web browser, set your address to "localhost:8000". This is the main page for the project.
5. The web site "gastronaut.com" should appear! Navigation by way of hyperlinks should be self-explanatory. However, you will not be able to create/add/delete categories and/or recipes unless you click the "Login" link at the top of the page. You must have a Facebook or Google+ account to log in. You may not edit nor delete anything you did not create with that same account!
6. To extract JSON data from this website, navigate to "localhost:8000/category/JSON" for a JSON of the food categories. Or "localhost:8000/category/<category #>/recipe/<recipe #>/JSON" for an individual recipe. For example: "http://localhost:8000/category/1/recipe/2/JSON" displays the JSON for a "Sidecar".
