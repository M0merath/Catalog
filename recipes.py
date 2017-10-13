from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, Recipe, User

engine = create_engine('sqlite:///gastronaut.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()



# 'Appetizers & Sides'
category1 = Category(name = "Appetizers & Sides")

session.add(category1)
session.commit()

recipe2 = Recipe(name = "Veggie Burger", description = "Juicy grilled veggie patty with tomato mayo and lettuce", cuisine = "Entree", category = category1)

session.add(recipe2)
session.commit()


recipe1 = Recipe(name = "French Fries", description = "with garlic and parmesan", cuisine = "Appetizer", category = category1)

session.add(recipe1)
session.commit()

recipe2 = Recipe(name = "Chicken Burger", description = "Juicy grilled chicken patty with tomato mayo and lettuce", cuisine = "Entree", category = category1)

session.add(recipe2)
session.commit()

recipe3 = Recipe(name = "Chocolate Cake", description = "fresh baked and served with ice cream", cuisine = "Dessert", category = category1)

session.add(recipe3)
session.commit()

recipe4 = Recipe(name = "Sirloin Burger", description = "Made with grade A beef", cuisine = "Entree", category = category1)

session.add(recipe4)
session.commit()

recipe5 = Recipe(name = "Root Beer", description = "16oz of refreshing goodness", cuisine = "Beverage", category = category1)

session.add(recipe5)
session.commit()

recipe6 = Recipe(name = "Iced Tea", description = "with Lemon", cuisine = "Beverage", category = category1)

session.add(recipe6)
session.commit()

recipe7 = Recipe(name = "Grilled Cheese Sandwich", description = "On texas toast with American Cheese", cuisine = "Entree", category = category1)

session.add(recipe7)
session.commit()

recipe8 = Recipe(name = "Veggie Burger", description = "Made with freshest of ingredients and home grown spices", cuisine = "Entree", category = category1)

session.add(recipe8)
session.commit()




# 'Breakfast'
category2 = Category(name = "Breakfast")

session.add(category2)
session.commit()


recipe1 = Recipe(name = "Chicken Stir Fry", description = "With your choice of noodles vegetables and sauces", cuisine = "Entree", category = category2)

session.add(recipe1)
session.commit()

recipe2 = Recipe(name = "Peking Duck", description = " A famous duck dish from Beijing[1] that has been prepared since the imperial era. The meat is prized for its thin, crisp skin, with authentic versions of the dish serving mostly the skin and little meat, sliced in front of the diners by the cook", cuisine = "Entree", category = category2)

session.add(recipe2)
session.commit()

recipe3 = Recipe(name = "Spicy Tuna Roll", description = "Seared rare ahi, avocado, edamame, cucumber with wasabi soy sauce ", cuisine = "Entree", category = category2)

session.add(recipe3)
session.commit()

recipe4 = Recipe(name = "Nepali Momo ", description = "Steamed dumplings made with vegetables, spices and meat. ", cuisine = "Entree", category = category2)

session.add(recipe4)
session.commit()

recipe5 = Recipe(name = "Beef Noodle Soup", description = "A Chinese noodle soup made of stewed or red braised beef, beef broth, vegetables and Chinese noodles.", cuisine = "Entree", category = category2)

session.add(recipe5)
session.commit()

recipe6 = Recipe(name = "Ramen", description = "a Japanese noodle soup dish. It consists of Chinese-style wheat noodles served in a meat- or (occasionally) fish-based broth, often flavored with soy sauce or miso, and uses toppings such as sliced pork, dried seaweed, kamaboko, and green onions.", cuisine = "Entree", category = category2)

session.add(recipe6)
session.commit()




# 'Burgers & Sandwiches'
category3 = Category(name = "Burgers & Sandwiches")

session.add(category3)
session.commit()


recipe1 = Recipe(name = "Pho", description = "a Vietnamese noodle soup consisting of broth, linguine-shaped rice noodles called banh pho, a few herbs, and meat.", cuisine = "Entree", category = category1)

session.add(recipe1)
session.commit()

recipe2 = Recipe(name = "Chinese Dumplings", description = "a common Chinese dumpling which generally consists of minced meat and finely chopped vegetables wrapped into a piece of dough skin. The skin can be either thin and elastic or thicker.", cuisine = "Appetizer", category = category1)

session.add(recipe2)
session.commit()

recipe3 = Recipe(name = "Gyoza", description = "The most prominent differences between Japanese-style gyoza and Chinese-style jiaozi are the rich garlic flavor, which is less noticeable in the Chinese version, the light seasoning of Japanese gyoza with salt and soy sauce, and the fact that gyoza wrappers are much thinner", cuisine = "Entree", category = category1)

session.add(recipe3)
session.commit()

recipe4 = Recipe(name = "Stinky Tofu", description = "Taiwanese dish, deep fried fermented tofu served with pickled cabbage.", cuisine = "Entree", category = category1)

session.add(recipe4)
session.commit()

recipe2 = Recipe(name = "Veggie Burger", description = "Juicy grilled veggie patty with tomato mayo and lettuce", cuisine = "Entree", category = category1)

session.add(recipe2)
session.commit()


# 'Pasta & Rice Dishes'
category4 = Category(name = "Pasta & Rice Dishes")

session.add(category4)
session.commit()


recipe1 = Recipe(name = "Tres Leches Cake", description = "Rich, luscious sponge cake soaked in sweet milk and topped with vanilla bean whipped cream and strawberries.", cuisine = "Dessert", category = category1)

session.add(recipe1)
session.commit()

recipe2 = Recipe(name = "Mushroom risotto", description = "Portabello mushrooms in a creamy risotto", cuisine = "Entree", category = category1)

session.add(recipe2)
session.commit()

recipe3 = Recipe(name = "Honey Boba Shaved Snow", description = "Milk snow layered with honey boba, jasmine tea jelly, grass jelly, caramel, cream, and freshly made mochi", cuisine = "Dessert", category = category1)

session.add(recipe3)
session.commit()

recipe4 = Recipe(name = "Cauliflower Manchurian", description = "Golden fried cauliflower florets in a midly spiced soya,garlic sauce cooked with fresh cilantro, celery, chilies,ginger & green onions", cuisine = "Appetizer", category = category1)

session.add(recipe4)
session.commit()

recipe5 = Recipe(name = "Aloo Gobi Burrito", description = "Vegan goodness. Burrito filled with rice, garbanzo beans, curry sauce, potatoes (aloo), fried cauliflower (gobi) and chutney. Nom Nom", cuisine = "Entree", category = category1)

session.add(recipe5)
session.commit()

recipe2 = Recipe(name = "Veggie Burger", description = "Juicy grilled veggie patty with tomato mayo and lettuce", cuisine = "Entree", category = category1)

session.add(recipe2)
session.commit()



# 'Meat & Seafood Dishes'
category5 = Category(name = "Meat & Seafood Dishes")

session.add(category5)
session.commit()


recipe1 = Recipe(name = "Shellfish Tower", description = "Lobster, shrimp, sea snails, crawfish, stacked into a delicious tower", cuisine = "Entree", category = category1)

session.add(recipe1)
session.commit()

recipe2 = Recipe(name = "Chicken and Rice", description = "Chicken... and rice", cuisine = "Entree", category = category1)

session.add(recipe2)
session.commit()

recipe3 = Recipe(name = "Mom's Spaghetti", description = "Spaghetti with some incredible tomato sauce made by mom", cuisine = "Entree", category = category1)

session.add(recipe3)
session.commit()

recipe4 = Recipe(name = "Choc Full O\' Mint (Smitten\'s Fresh Mint Chip ice cream)", description = "Milk, cream, salt, ..., Liquid nitrogen magic", cuisine = "Dessert", category = category1)

session.add(recipe4)
session.commit()

recipe5 = Recipe(name = "Tonkatsu Ramen", description = "Noodles in a delicious pork-based broth with a soft-boiled egg", cuisine = "Entree", category = category1)

session.add(recipe5)
session.commit()




# 'Soups & Sauces'
category6 = Category(name = "Soups & Sauces")

session.add(category6)
session.commit()


recipe1 = Recipe(name = "Lamb Curry", description = "Slow cook that thang in a pool of tomatoes, onions and alllll those tasty Indian spices. Mmmm.", cuisine = "Entree", category = category1)

session.add(recipe1)
session.commit()

recipe2 = Recipe(name = "Chicken Marsala", description = "Chicken cooked in Marsala wine sauce with mushrooms", cuisine = "Entree", category = category1)

session.add(recipe2)
session.commit()

recipe3 = Recipe(name = "Potstickers", description = "Delicious chicken and veggies encapsulated in fried dough.", cuisine = "Appetizer", category = category1)

session.add(recipe3)
session.commit()

recipe4 = Recipe(name = "Nigiri Sampler", description = "Maguro, Sake, Hamachi, Unagi, Uni, TORO!", cuisine = "Appetizer", category = category1)

session.add(recipe4)
session.commit()

recipe2 = Recipe(name = "Veggie Burger", description = "Juicy grilled veggie patty with tomato mayo and lettuce", cuisine = "Entree", category = category1)

session.add(recipe2)
session.commit()




# 'Desserts'
category7 = Category(name = "Desserts")

session.add(category7)
session.commit()

recipe9 = Recipe(name = "Chicken Fried Steak", description = "Fresh battered sirloin steak fried and smothered with cream gravy", cuisine = "Entree", category = category1)

session.add(recipe9)
session.commit()



recipe1 = Recipe(name = "Boysenberry Sorbet", description = "An unsettlingly huge amount of ripe berries turned into frozen (and seedless) awesomeness", cuisine = "Dessert", category = category1)

session.add(recipe1)
session.commit()

recipe2 = Recipe(name = "Broiled salmon", description = "Salmon fillet marinated with fresh herbs and broiled hot & fast", cuisine = "Entree", category = category1)

session.add(recipe2)
session.commit()

recipe3 = Recipe(name = "Morels on toast (seasonal)", description = "Wild morel mushrooms fried in butter, served on herbed toast slices", cuisine = "Appetizer", category = category1)

session.add(recipe3)
session.commit()

recipe4 = Recipe(name = "Tandoori Chicken", description = "Chicken marinated in yoghurt and seasoned with a spicy mix(chilli, tamarind among others) and slow cooked in a cylindrical clay or metal oven which gets its heat from burning charcoal.", cuisine = "Entree", category = category1)

session.add(recipe4)
session.commit()

recipe2 = Recipe(name = "Veggie Burger", description = "Juicy grilled veggie patty with tomato mayo and lettuce", cuisine = "Entree", category = category1)

session.add(recipe2)
session.commit()

recipe10 = Recipe(name = "Spinach Ice Cream", description = "vanilla ice cream made with organic spinach leaves", cuisine = "Dessert", category = category1)

session.add(recipe10)
session.commit()



# 'Beverages & Cocktails'
category8 = Category(name = "Beverages & Cocktails")

session.add(category8)
session.commit()


recipe1 = Recipe(name = "Super Burrito Al Pastor", description = "Marinated Pork, Rice, Beans, Avocado, Cilantro, Salsa, Tortilla", cuisine = "Entree", category = category1)

session.add(recipe1)
session.commit()

recipe2 = Recipe(name = "Cachapa", description = "Golden brown, corn-based Venezuelan pancake; usually stuffed with queso telita or queso de mano, and possibly lechon. ", cuisine = "Entree", category = category1)

session.add(recipe2)
session.commit()


recipe1 = Recipe(name = "State Bird Provisions")
session.add(category1)
session.commit()

recipe1 = Recipe(name = "Chantrelle Toast", description = "Crispy Toast with Sesame Seeds slathered with buttery chantrelle mushrooms", cuisine = "Appetizer", category = category1)

session.add(recipe1)
session.commit

recipe1 = Recipe(name = "Guanciale Chawanmushi", description = "Japanese egg custard served hot with spicey Italian Pork Jowl (guanciale)", cuisine = "Dessert", category = category1)

session.add(recipe1)
session.commit()



recipe1 = Recipe(name = "Lemon Curd Ice Cream Sandwich", description = "Lemon Curd Ice Cream Sandwich on a chocolate macaron with cardamom meringue and cashews", cuisine = "Dessert", category = category1)

session.add(recipe1)
session.commit()


print "added menu items!"
