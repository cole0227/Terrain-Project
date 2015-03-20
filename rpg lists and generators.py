# -*- coding: cp1252 -*-
import random
import copy
import itertools
import profile


materialType = ("Naked", "Woven Lint", "Hair", "Wax", "Cotton", "Wool", "Paper", "Egg Carton", "Cardboard",
                "Soft Plastic", "Rodent Pelt", "Deer Pelt", "Snake Hide", "Wolf Pelt", "Buffalo Pelt", "Leather",
                "Balsa", "Bamboo", "Ivory", "Stone", "Cured Leather", "Rhino Hide", "Crocodile Hide", "Shark Hide",
                "Fir Wood", "Pine Wood", "Cedar Wood", "Spruce Wood", "Tin", "Lead", "Gold", "Copper", "Silver",
                "Teac Wood", "Maple", "Beechwood", "Oak", "Royal Oak", "Walnut", "Mahogany", "Rosewood", "Tamarind",
                "Ironwood", "Ebony", "Hardened Plastic", "Pure Aluminium", "Duralmin", "Silumin", "Hiduminium",
                "Cast Brass", "Common Brass", "Naval Brass", "High Tensile Brass", "Phosphor Bronze", "Leaded Bronze",
                "Silicon Bronze", "Aluminium Bronze", "Manganese Bronze", "Pig Iron", "Grey Cast Iron",
                "White Cast Iron", "Nondular Iron", "Magnesium Alloy", "Low Carbon Steel", "Mild Steel",
                "Medium Carbon Steel", "High Carbon Steel", "Ultra High Carbon Steel", "Spring Steel",
                "Stainless Steel", "Weathering Steel", "High Tensile Steel", "Wootz Steel", "Kevlar", "Ceramic",
                "Kevlar and Ceramic", "Depleted Uranium", "Nanotube", "Starlite", "Reactive Crystal", "Nanite")

qualityType = ("Shattered", "Broken", "Bent", "Cracked", "Worn", "Poor", "Okay", "Good", "Great", "Pristine", "Splendid", "Flawless", "Radiant", "Divine")
qualityMod  = (       -1.5,     -1.3,   -1.1,      -0.9,   -0.6,   -0.3,   -0.1,      0,     0.3,        0.5,        0.7,        0.9,       1.2,      1.5)

itemType = ("Helmet", "Armour Shirt", "Armour Pants", "Shield", "Sword", "Knife", "Axe", "Sling", "Spear", "Bow", "Ward")

itemEffect = ("Tough", "Enduring", "Immortal",
              "Fertile", "Verdant", "Overgrown",
              "Shiny", "Glowing", "Sparkling",
              "Solar", "Lunar", "Starlit", "Martian", "Shadow",
              "Heated", "Flaming", "Molten",
              "Sparking", "Arcing", "Thunderous",
              "Chill", "Frosty", "Frigid",
              "Sharp", "Keen", "Dismembering",
              "Normal", "Fire", "Fighting", "Water", "Flying", "Grass", "Poison", "Electric", "Ground", "Psychic", "Rock", "Ice", "Bug", "Dragon", "Ghost", "Dark", "Steel", "Fairy",
              "Gooey","Slimey","Lesser","Greater","Giant","Tiny","Oozing","Spikey","Cosmic","Melting","Smelly","Stinky","Crusty")

#first names from US census beaureau (~1950) and wikipedia (~1050)
firstNames = ("James", "John", "Robert", "Michael", "William", "David", "Richard", "Charles", "Joseph", "Thomas", "Christopher", "Daniel", "Paul", "Mark", "Donald", "George", "Kenneth", "Steven", "Edward", "Brian", "Ronald", "Anthony", "Kevin", "Jason",
              "Matthew", "Gary", "Timothy", "Jose", "Larry", "Jeffrey", "Frank", "Scott", "Eric", "Stephen", "Andrew", "Raymond", "Gregory", "Joshua", "Jerry", "Dennis", "Walter", "Patrick", "Peter", "Harold", "Douglas", "Henry", "Carl", "Arthur",
              "Ryan", "Roger", "Joe", "Juan", "Jack", "Albert", "Jonathan", "Justin", "Terry", "Gerald", "Keith", "Samuel", "Willie", "Lawrence", "Ralph", "Nicholas", "Roy", "Benjamin", "Bruce", "Brandon", "Adam", "Fred", "Harry", "Wayne", "Billy",
              "Steve", "Louis", "Jeremy", "Aaron", "Randy", "Eugene", "Howard", "Carlos", "Russell", "Bobby", "Victor", "Martin", "Ernest", "Phillip", "Todd", "Jesse", "Craig", "Alan", "Shawn", "Chris", "Clarence", "Philip", "Sean", "Johnny", "Earl",
              "Jimmy", "Antonio", "Bryan", "Danny", "Tony", "Luis", "Mike", "Leonard", "Stanley", "Nathan", "Dale", "Manuel", "Curtis", "Rodney", "Norman", "Allen", "Marvin", "Vincent", "Glenn", "Jeff", "Jeffery", "Travis", "Chad", "Jacob", "Alfred",
              "Lee", "Melvin", "Francis", "Kyle", "Bradley", "Herbert", "Jesus", "Frederick", "Ray", "Joel", "Edwin", "Don", "Eddie", "Ricky", "Randall", "Troy", "Barry", "Alexander", "Bernard", "Leroy", "Mario", "Francisco", "Marcus", "Clifford",
              "Micheal", "Theodore", "Miguel", "Oscar", "Jay", "Jim", "Tom", "Alex", "Calvin", "Jon", "Ronnie", "Bill", "Derek", "Leon", "Lloyd", "Tommy", "Warren", "Darrell", "Jerome", "Floyd", "Leo", "Alvin", "Dean", "Gordon", "Greg", "Jorge", "Tim",
              "Wesley", "Derrick", "Dustin", "Pedro", "Dan", "Lewis", "Zachary", "Corey", "Herman", "Maurice", "Roberto", "Vernon", "Clyde", "Glen", "Hector", "Ricardo", "Shane", "Sam", "Lester", "Rick", "Brent", "Charlie", "Ramon", "Gilbert", "Tyler",
              "Gene", "Marc", "Reginald", "Angel", "Brett", "Ruben", "Leslie", "Nathaniel", "Rafael", "Edgar", "Milton", "Raul", "Ben", "Cecil", "Chester", "Duane", "Franklin", "Andre", "Elmer", "Brad", "Gabriel", "Arnold", "Harvey", "Mitchell",
              "Roland", "Ron", "Jared", "Adrian", "Karl", "Claude", "Cory", "Erik", "Darryl", "Jamie", "Neil", "Christian", "Clinton", "Fernando", "Javier", "Jessie", "Darren", "Lonnie", "Mathew", "Ted", "Tyrone", "Cody", "Julio", "Kelly", "Lance",
              "Kurt", "Allan", "Nelson", "Clayton", "Guy", "Hugh", "Dwayne", "Max", "Armando", "Dwight", "Felix", "Jimmie", "Everett", "Ian", "Jordan", "Wallace", "Bob", "Jaime", "Ken", "Alfredo", "Casey", "Alberto", "Dave", "Ivan", "Byron", "Johnnie",
              "Julian", "Sidney", "Isaac", "Morris", "Clifton", "Daryl", "Ross", "Willard", "Andy", "Kirk", "Marshall", "Perry", "Salvador", "Sergio", "Virgil", "Kent", "Marion", "Rene", "Seth", "Terrance", "Tracy", "Eduardo", "Terrence", "Enrique",
              "Freddie", "Wade", "Austin", "Stuart", "Alejandro", "Arturo", "Fredrick", "Jackie", "Joey", "Luther", "Nick", "Dana", "Evan", "Jeremiah", "Julius", "Wendell", "Donnie", "Otis", "Doug", "Gerard", "Homer", "Luke", "Oliver", "Shannon",
              "Trevor", "Angelo", "Hubert", "Kenny", "Shaun", "Alfonso", "Lyle", "Lynn", "Matt", "Cameron", "Carlton", "Ernesto", "Neal", "Orlando", "Rex", "Blake", "Grant", "Horace", "Kerry", "Lorenzo", "Omar", "Pablo", "Roderick", "Wilbur", "Abraham",
              "Ira", "Jean", "Rickey", "Willis", "Andres", "Cesar", "Damon", "Johnathan", "Kelvin", "Malcolm", "Preston", "Rudolph", "Rudy", "Alton", "Archie", "Marco", "Wam", "Bennie", "Dominic", "Ed", "Felipe", "Garry", "Geoffrey", "Gerardo",
              "Jonathon", "Loren", "Pete", "Randolph", "Robin", "Colin", "Delbert", "Earnest", "Guillermo", "Lucas", "Benny", "Edmund", "Myron", "Noel", "Rodolfo", "Spencer", "Cedric", "Garrett", "Gregg", "Lowell", "Salvatore", "Devin", "Israel",
              "Jermaine", "Kim", "Roosevelt", "Sherman", "Sylvester", "Wilson", "Forrest", "Leland", "Wilbert", "Bryant", "Carroll", "Clark", "Guadalupe", "Irving", "Owen", "Simon", "Gustavo", "Jake", "Kristopher", "Levi", "Mack", "Marcos", "Rufus",
              "Sammy", "Woodrow", "Clint", "Dallas", "Drew", "Ellis", "Gilberto", "Ismael", "Jody", "Laurence", "Lionel", "Marty", "Nicolas", "Orville", "Taylor", "Al", "Caleb", "Dewey", "Erick", "Ervin", "Frankie", "Hugo", "Ignacio", "Josh", "Sheldon",
              "Tomas", "Wilfred", "Alonzo", "Bert", "Conrad", "Darrel", "Doyle", "Elbert", "Elias", "Noah", "Pat", "Ramiro", "Rogelio", "Santiago", "Stewart", "Terence", "Bradford", "Clay", "Cornelius", "Dexter", "Grady", "Lamar", "Merle", "Percy",
              "Phil", "Rolando", "Amos", "Darin", "Darnell", "Irvin", "Moses", "Randal", "Roman", "Saul", "Terrell", "Tommie", "Abel", "Aubrey", "Boyd", "Brendan", "Cary", "Courtney", "Darrin", "Domingo", "Dominick", "Edmond", "Elijah", "Emanuel",
              "Emil", "Emilio", "Emmett", "Jan", "Jerald", "Marlon", "Santos", "Timmy", "Toby", "Van", "Winston", "Bret", "Dewayne", "Emmanuel", "Humberto", "Jess", "Louie", "Morgan", "Otto", "Reynaldo", "Stephan", "Teddy", "Trent", "Will", "Billie",
              "Demetrius", "Efrain", "Eldon", "Ethan", "Garland", "Harley", "Heath", "Lamont", "Logan", "Micah", "Miles", "Rodger", "Stacy", "Vicente", "Antoine", "Bryce", "Chase", "Chuck", "Cleveland", "Damian", "Dylan", "Eli", "Elton", "Freddy",
              "Grover", "Junior", "Kendall", "Mickey", "Pierre", "Robbie", "Rocky", "Royce", "Sterling", "Agustin", "August", "Benito", "Blaine", "Curt", "Ernie", "Erwin", "Hans", "Jasper", "Leonardo", "Monte", "Murray", "Quentin", "Reuben", "Russel",
              "Stan", "Adolfo", "Ashley", "Bart", "Brady", "Buddy", "Burton", "Damien", "Darwin", "Denis", "Desmond", "Devon", "Elliot", "Elliott", "Gregorio", "Harlan", "Harrison", "Jamal", "Jarrod", "Joaquin", "Tyson", "Vance", "Wilfredo", "Anton",
              "Brain", "Carey", "Darius", "Elvin", "Elwood", "Esteban", "Hal", "Kendrick", "Kermit", "Moises", "Nolan", "Norbert", "Quinton", "Rob", "Rod", "Roscoe", "Scotty", "Solomon", "Williams", "Xavier", "Ali", "Alvaro", "Armand", "Bryon", "Cliff",
              "Dane", "Fabian", "Fidel", "Graham", "Jackson", "Jeffry", "Joesph", "Marcel", "Marlin", "Mason", "Michel", "Monty", "Ned", "Raphael", "Reggie", "Rory", "Rusty", "Sammie", "Son", "Thaddeus", "Thurman", "Adolph", "Alexis", "Alphonso",
              "Avery", "Carmen", "Derick", "Diego", "Gerry", "Gonzalo", "Gus", "Isaiah", "Kris", "Loyd", "Millard", "Noe", "Norris", "Rickie", "Rigoberto", "Rocco", "Rodrigo", "Shelby", "Stacey", "Ty", "Vaughn", "Wiley", "Basil", "Bernardo", "Bobbie",
              "Bruno", "Clement", "Cole", "Coy", "Dante", "Davis", "Denny", "Dion", "Donnell", "Donovan", "Eddy", "Elvis", "Emery", "Federico", "Gavin", "Heriberto", "Hiram", "Issac", "Jarvis", "Jayson", "Jefferson", "Mauricio", "Maxwell", "Maynard",
              "Nickolas", "Odell", "Ollie", "Quincy", "Reed", "Riley", "Romeo", "Scot", "Sebastian", "Ulysses", "Vern", "Vince", "Ward", "Art", "Aurelio", "Barney", "Beau", "Brock", "Carlo", "Carmelo", "Carter", "Charley", "Cleo", "Colby", "Collin",
              "Cruz", "Delmar", "Denver", "Dick", "Donny", "Dudley", "Frederic", "Galen", "Harris", "Hollis", "Hunter", "Irwin", "Isidro", "Johnathon", "Kirby", "Kurtis", "Lane", "Linwood", "Marcelino", "Mary", "Merlin", "Merrill", "Nestor", "Sanford",
              "Silas", "Stefan", "Trenton", "Truman", "Vito", "Weldon", "Winfred", "Adan", "Antony", "Arron", "Bennett", "Bernie", "Blair", "Booker", "Branden", "Buford", "Carson", "Clair", "Cornell", "Dalton", "Danial", "Daren", "Dirk", "Dominique",
              "Edwardo", "Emerson", "Emory", "Errol", "Fletcher", "Gale", "Genaro", "German", "Houston", "Hung", "Jacques", "Jame", "Joan", "Josue", "Landon", "Laverne", "Leonel", "Lincoln", "Mariano", "Mohammad", "Monroe", "Numbers", "Octavio",
              "Pasquale", "Raymundo", "Robby", "Shelton", "Sonny", "Theron", "Tristan", "Wilford", "Wilmer", "Zachery", "Abdul", "Aldo", "Alphonse", "Alva", "Anderson", "Ariel", "Arnulfo", "Augustine", "Brooks", "Carmine", "Chadwick", "Chance",
              "Cyril", "Cyrus", "Duncan", "Dusty", "Erich", "Erin", "Eugenio", "Ezra", "Ferdinand", "Forest", "Freeman", "Garth", "Giovanni", "Herschel", "Jamel", "Jarrett", "Johnie", "Jonas", "Kennith", "Lazaro", "Lindsey", "Lon", "Luciano", "Lucien",
              "Major", "Mervin", "Mitchel", "Mohammed", "Morton", "Myles", "Randell", "Reid", "Rich", "Ronny", "Russ", "Sandy", "Scottie", "Seymour", "Stevie", "Sydney", "Thad", "Tracey", "Valentin", "Wilburn", "Young", "Zane", "Abe", "Ahmad", "Alden",
              "Alec", "Alfonzo", "Andrea", "Antwan", "Aron", "Barton", "Berry", "Boris", "Brant", "Brenton", "Burt", "Carol", "Christoper", "Claudio", "Coleman", "Deandre", "Deon", "Dewitt", "Dino", "Donn", "Dorian", "Earle", "Edgardo", "Efren",
              "Eliseo", "Elmo", "Eloy", "Emile", "Everette", "Faustino", "Foster", "Fritz", "Gail", "Gil", "Gino", "Hershel", "Isiah", "Ivory", "Jamaal", "Jamar", "Jarred", "Jerold", "Jerrod", "Josef", "Josiah", "Judson", "Jules", "Kareem", "Kieth",
              "Lanny", "Lavern", "Lemuel", "Leopoldo", "Les", "Lucio", "Lyman", "Margarito", "Marquis", "Milford", "Mitch", "Napoleon", "Nigel", "Norberto", "Normand", "Olin", "Osvaldo", "Parker", "Refugio", "Reinaldo", "Rico", "Rodrick", "Rosendo",
              "Royal", "Rubin", "Sang", "Tanner", "Trey", "Weston", "Wilton", "Wyatt", "Yong", "Abram", "Adalberto", "Ahmed", "Amado", "Anibal", "Antone", "Augustus", "Barrett", "Bertram", "Bo", "Bradly", "Brendon", "Brice", "Bud", "Burl", "Chang",
              "Chauncey", "Chet", "Chi", "Chung", "Cletus", "Columbus", "Connie", "Damion", "Dannie", "Dario", "Darrick", "Dee", "Delmer", "Demarcus", "Dillon", "Donte", "Dwain", "Enoch", "Fermin", "Florencio", "Frances", "Fredric", "Garfield",
              "Geraldo", "Giuseppe", "Hank", "Hassan", "Hilario", "Hilton", "Hipolito", "Horacio", "Huey", "Isaias", "Jamey", "Jamison", "Jed", "Jefferey", "Jerrold", "Jonah", "Keenan", "Kenton", "Keven", "Kip", "Kory", "Lawerence", "Lenard", "Lenny",
              "Lou", "Lupe", "Lyndon", "Mac", "Marcelo", "Maria", "Markus", "Mauro", "Maximo", "Mckinley", "Mel", "Mikel", "Milo", "Minh", "Mohamed", "Moshe", "Newton", "Noble", "Odis", "Olen", "Omer", "Oren", "Orval", "Porfirio", "Prince", "Quinn",
              "Quintin", "Raleigh", "Reyes", "Richie", "Robt", "Rolland", "Rosario", "Rupert", "Sal", "Shirley", "Sol", "Stanford", "Sung", "Tad", "Teodoro", "Thanh", "Theo", "Tobias", "Tod", "Tory", "Trinidad", "Tyree", "Tyrell", "Tyron", "Valentine",
              "Waldo", "Walker", "Werner", "Whitney", "Willy", "Zachariah", "Mary", "Patricia", "Linda", "Barbara", "Elizabeth", "Jennifer", "Maria", "Susan", "Margaret", "Dorothy", "Lisa", "Nancy", "Karen", "Betty", "Helen", "Sandra", "Donna", "Carol",
              "Ruth", "Sharon", "Michelle", "Laura", "Sarah", "Kimberly", "Deborah", "Jessica", "Shirley", "Cynthia", "Angela", "Melissa", "Brenda", "Amy", "Anna", "Rebecca", "Virginia", "Kathleen", "Pamela", "Martha", "Debra", "Amanda", "Stephanie",
              "Carolyn", "Christine", "Janet", "Marie", "Catherine", "Frances", "Ann", "Joyce", "Diane", "Alice", "Julie", "Heather", "Teresa", "Doris", "Gloria", "Evelyn", "Cheryl", "Jean", "Katherine", "Mildred", "Joan", "Ashley", "Judith", "Rose",
              "Janice", "Kelly", "Nicole", "Judy", "Christina", "Kathy", "Theresa", "Beverly", "Denise", "Tammy", "Irene", "Jane", "Lori", "Rachel", "Marilyn", "Andrea", "Kathryn", "Louise", "Sara", "Anne", "Jacqueline", "Wanda", "Bonnie", "Julia",
              "Ruby", "Lois", "Tina", "Phyllis", "Norma", "Paula", "Annie", "Diana", "Lillian", "Emily", "Peggy", "Robin", "Crystal", "Gladys", "Rita", "Dawn", "Connie", "Florence", "Edna", "Tracy", "Carmen", "Tiffany", "Rosa", "Cindy", "Grace",
              "Wendy", "Victoria", "Edith", "Kim", "Sherry", "Josephine", "Sylvia", "Shannon", "Sheila", "Thelma", "Ethel", "Elaine", "Ellen", "Marjorie", "Carrie", "Charlotte", "Esther", "Monica", "Emma", "Pauline", "Juanita", "Anita", "Rhonda",
              "Hazel", "Amber", "Eva", "Debbie", "April", "Leslie", "Clara", "Jamie", "Lucille", "Eleanor", "Joanne", "Danielle", "Valerie", "Megan", "Alicia", "Gail", "Michele", "Suzanne", "Bertha", "Darlene", "Jill", "Veronica", "Erin", "Geraldine",
              "Cathy", "Lauren", "Joann", "Lorraine", "Lynn", "Sally", "Regina", "Beatrice", "Erica", "Dolores", "Bernice", "Audrey", "Yvonne", "Annette", "June", "Samantha", "Dana", "Marion", "Stacy", "Ana", "Renee", "Ida", "Vivian", "Brittany",
              "Holly", "Roberta", "Melanie", "Jeanette", "Loretta", "Yolanda", "Laurie", "Katie", "Alma", "Kristen", "Sue", "Vanessa", "Beth", "Elsie", "Jeanne", "Vicki", "Carla", "Rosemary", "Tara", "Eileen", "Terri", "Gertrude", "Lucy", "Tonya",
              "Ella", "Stacey", "Gina", "Kristin", "Wilma", "Agnes", "Jessie", "Natalie", "Vera", "Charlene", "Willie", "Bessie", "Delores", "Arlene", "Melinda", "Pearl", "Allison", "Colleen", "Maureen", "Tamara", "Constance", "Georgia", "Joy",
              "Claudia", "Jackie", "Lillie", "Marcia", "Minnie", "Nellie", "Tanya", "Glenda", "Heidi", "Marlene", "Courtney", "Lydia", "Marian", "Viola", "Caroline", "Stella", "Dora", "Jo", "Vickie", "Mattie", "Terry", "Irma", "Maxine", "Mabel",
              "Marsha", "Myrtle", "Christy", "Lena", "Deanna", "Patsy", "Hilda", "Gwendolyn", "Jennie", "Nora", "Cassandra", "Leah", "Margie", "Nina", "Carole", "Kay", "Naomi", "Penny", "Priscilla", "Brandy", "Olga", "Billie", "Dianne", "Leona",
              "Tracey", "Felicia", "Jenny", "Sonia", "Becky", "Miriam", "Velma", "Bobbie", "Kristina", "Violet", "Toni", "Mae", "Misty", "Daisy", "Ramona", "Shelly", "Sherri", "Claire", "Erika", "Katrina", "Lindsay", "Lindsey", "Belinda", "Geneva",
              "Guadalupe", "Margarita", "Sheryl", "Cora", "Faye", "Ada", "Isabel", "Natasha", "Sabrina", "Harriet", "Hattie", "Marguerite", "Blanche", "Brandi", "Cecilia", "Iris", "Joanna", "Kristi", "Molly", "Rosie", "Sandy", "Angie", "Eunice", "Inez",
              "Lynda", "Alberta", "Amelia", "Madeline", "Candace", "Genevieve", "Jan", "Janie", "Jodi", "Kayla", "Kristine", "Lee", "Maggie", "Monique", "Sonya", "Alison", "Fannie", "Maryann", "Melody", "Opal", "Yvette", "Flora", "Luz", "Olivia",
              "Shelley", "Susie", "Antoinette", "Beulah", "Kristy", "Lola", "Lula", "Mamie", "Verna", "Candice", "Jeannette", "Juana", "Kelli", "Pam", "Bridget", "Hannah", "Whitney", "Celia", "Karla", "Della", "Gayle", "Latoya", "Lynne", "Patty",
              "Shelia", "Vicky", "Marianne", "Sheri", "Blanca", "Erma", "Jacquelyn", "Kara", "Krista", "Leticia", "Myra", "Pat", "Roxanne", "Adrienne", "Alexandra", "Angelica", "Bernadette", "Bethany", "Brooke", "Francis", "Johnnie", "Robyn", "Rosalie",
              "Sadie", "Chelsea", "Ernestine", "Jasmine", "Jody", "Kendra", "Mable", "Muriel", "Nichole", "Rachael", "Traci", "Angelina", "Elena", "Krystal", "Marcella", "Dianna", "Estelle", "Kari", "Lora", "Nadine", "Paulette", "Angel", "Antonia",
              "Desiree", "Doreen", "Mona", "Rosemarie", "Betsy", "Christie", "Freda", "Ginger", "Hope", "Janis", "Cristina", "Eula", "Lynette", "Mercedes", "Meredith", "Teri", "Cecelia", "Eloise", "Gretchen", "Leigh", "Meghan", "Rochelle", "Sophia",
              "Alyssa", "Gwen", "Henrietta", "Jana", "Kelley", "Kerry", "Raquel", "Alexis", "Jenna", "Laverne", "Olive", "Tasha", "Tricia", "Casey", "Darla", "Delia", "Elvira", "Essie", "Kate", "Kellie", "Lana", "Lila", "Lorena", "Mandy", "May", "Mindy",
              "Patti", "Silvia", "Sonja", "Sophie", "Camille", "Dixie", "Elsa", "Faith", "Jeannie", "Johanna", "Josefina", "Lela", "Lorene", "Lucia", "Marta", "Miranda", "Shari", "Aimee", "Alisha", "Ebony", "Elisa", "Jaime", "Kristie", "Marina", "Melba",
              "Nettie", "Ollie", "Ora", "Rena", "Shawna", "Tabitha", "Tami", "Winifred", "Addie", "Bonita", "Latasha", "Marla", "Myrna", "Patrice", "Ronda", "Sherrie", "Tammie", "Abigail", "Adele", "Adriana", "Cara", "Celeste", "Cheri", "Deloris",
              "Dorthy", "Francine", "Jewel", "Lucinda", "Rebekah", "Shelby", "Stacie", "Aurora", "Brittney", "Chris", "Corinne", "Effie", "Elva", "Estella", "Etta", "Fern", "Francisca", "Helene", "Janelle", "Josie", "Karin", "Kelsey", "Kerri", "Laurel",
              "Lenora", "Lottie", "Lourdes", "Marissa", "Nikki", "Reba", "Sallie", "Shawn", "Tracie", "Trina", "Trisha", "Aida", "Bettie", "Caitlin", "Cassie", "Christa", "Elisabeth", "Eugenia", "Goldie", "Ina", "Ingrid", "Iva", "Jenifer", "Maude",
              "Candy", "Cherie", "Consuelo", "Debora", "Dena", "Dina", "Frankie", "Janette", "Latonya", "Lorna", "Morgan", "Polly", "Rosetta", "Tamika", "Therese", "Carolina", "Cleo", "Dorothea", "Esperanza", "Fay", "Helena", "Jewell", "Jillian",
              "Kimberley", "Nell", "Patrica", "Shanna", "Stefanie", "Trudy", "Alisa", "Janine", "Lou", "Lupe", "Maribel", "Mollie", "Ola", "Rosario", "Susanne", "Alta", "Bette", "Cecile", "Daphne", "Elise", "Ester", "Graciela", "Imogene", "Isabelle",
              "Jocelyn", "Jolene", "Joni", "Keisha", "Leola", "Lesley", "Paige", "Petra", "Rachelle", "Susana", "Adeline", "Beatriz", "Carmela", "Charity", "Clarice", "Gabriela", "Glenna", "Gracie", "Jaclyn", "Jayne", "Keri", "Kirsten", "Lacey",
              "Lizzie", "Marisa", "Marisol", "Mayra", "Rosalind", "Shana", "Sondra", "Tonia", "Ursula", "Angelia", "Angeline", "Autumn", "Cathleen", "Christi", "Claudette", "Elma", "Frieda", "Gabrielle", "Jeanine", "Jimmie", "Jodie", "Justine",
              "Katharine", "Lea", "Lily", "Luella", "Margret", "Millie", "Robbie", "Shauna", "Sheena", "Staci", "Summer", "Abby", "Aileen", "Bobbi", "Callie", "Dale", "Deana", "Dee", "Dolly", "Dominique", "Gale", "Ivy", "Jeannine", "Ladonna", "Lara",
              "Leanne", "Lorie", "Lucile", "Luisa", "Manuela", "Marcy", "Margo", "Maritza", "Martina", "Mavis", "Rene", "Selma", "Socorro", "Sybil", "Willa", "Winnie", "Audra", "Barbra", "Bettye", "Bianca", "Bridgette", "Cornelia", "Eliza", "Georgina",
              "Jeri", "Latisha", "Leann", "Leila", "Magdalena", "Matilda", "Meagan", "Ofelia", "Randi", "Simone", "Virgie", "Adela", "Alexandria", "Ava", "Bernadine", "Brianna", "Catalina", "Chandra", "Clarissa", "Concepcion", "Corrine", "Dona",
              "Earline", "Elnora", "Ericka", "Estela", "Flossie", "Greta", "Haley", "Hilary", "Ila", "Jami", "Lenore", "Letha", "Lidia", "Lilly", "Mia", "Minerva", "Nelda", "Nola", "Rae", "Rhoda", "Rosalyn", "Ruthie", "Sharron", "Terrie", "Tia",
              "Valarie", "Allie", "Allyson", "Amie", "Ashlee", "Avis", "Benita", "Emilia", "Esmeralda", "Eve", "Harriett", "Hillary", "Jeanie", "Karina", "Loraine", "Malinda", "Marylou", "Melisa", "Milagros", "Nannie", "Neva", "Noreen", "Odessa",
              "Pearlie", "Penelope", "Saundra", "Serena", "Sofia", "Tabatha", "Tameka", "Tania", "Tommie", "Zelma", "Alana", "Alejandra", "Althea", "Annabelle", "Carlene", "Carmella", "Clare", "Darcy", "Earlene", "Earnestine", "Elinor", "Gay", "Jerri",
              "John", "Jordan", "Julianne", "Katy", "Lilia", "Liza", "Lorrie", "Louisa", "Mallory", "Marcie", "Michael", "Nita", "Noemi", "Rosalinda", "Selena", "Tanisha", "Taylor", "Aline", "Alissa", "Charmaine", "Chrystal", "Claudine", "Colette",
              "Corine", "Deanne", "Dollie", "Eddie", "Edwina", "Evangeline", "Fran", "Georgette", "Ilene", "Jerry", "Juliana", "Kasey", "Kathie", "Kathrine", "Kaye", "Kenya", "Kris", "Lakisha", "Lavonne", "Lawanda", "Lilian", "Lina", "Luann", "Madge",
              "Margery", "Mari", "Maricela", "Maryanne", "Melva", "Merle", "Mitzi", "Nadia", "Nanette", "Nona", "Ophelia", "Roslyn", "Roxie", "Suzette", "Tammi", "Valeria", "Yesenia", "Alyce", "Amalia", "Anastasia", "Araceli", "Arline", "Augusta",
              "Aurelia", "Berta", "Briana", "Carly", "Chasity", "Christian", "Corina", "Deena", "Deidre", "Deirdre", "Elvia", "Gena", "Imelda", "James", "Janna", "Josefa", "Juliette", "Katelyn", "Lakeisha", "Leonor", "Lessie", "Liliana", "Lynnette",
              "Madelyn", "Marci", "Marietta", "Marva", "Natalia", "Reva", "Rosanne", "Roseann", "Rosella", "Sasha", "Savannah", "Sheree", "Susanna", "Tessa", "Vilma", "Wendi", "Young", "Adrian", "Aisha", "Alba", "Alfreda", "Alyson", "Amparo",
              "Angelique", "Angelita", "Annmarie", "Bertie", "Beryl", "Bridgett", "Brigitte", "Britney", "Carey", "Carissa", "Casandra", "Cathryn", "Cherry", "Coleen", "Concetta", "Diann", "Dionne", "Enid", "Erna", "Evangelina", "Fanny", "Florine",
              "Francesca", "Freida", "Gilda", "Hallie", "Helga", "Hester", "Hollie", "Ines", "Jacklyn", "Janell", "Jannie", "Juliet", "Kaitlin", "Karyn", "Katheryn", "Katina", "Lacy", "Lauri", "Leanna", "Lelia", "Liz", "Lolita", "Madeleine", "Mai",
              "Mara", "Mariana", "Marquita", "Maryellen", "Maura", "Millicent", "Phoebe", "Queen", "Reyna", "Rhea", "Rosanna", "Rowena", "Tamera", "Tamra", "Tisha", "Twila", "Wilda", "Abbie", "Adelaide", "Allene", "Antionette", "Ashleigh", "Beverley",
              "Bobby", "Brandie", "Camilla", "Caryn", "Celina", "Chelsey", "Cortney", "Dayna", "Deann", "Deidra", "Denice", "Dessie", "Doretha", "Edythe", "Elba", "Elda", "Elisha", "Emilie", "Felecia", "Gayla", "Geri", "Germaine", "Gussie", "Herminia",
              "Isabella", "Jade", "Jasmin", "Jesse", "Judi", "Justina", "Kaitlyn", "Kathi", "Kimberlee", "Kitty", "Lakesha", "Lashonda", "Latanya", "Leeann", "Lesa", "Leta", "Letitia", "Libby", "Louella", "Ma", "Margot", "Mellisa", "Michaela", "Michell",
              "Mina", "Monika", "Nan", "Nelly", "Noelle", "Octavia", "Pamala", "Pansy", "Renae", "Robert", "Rocio", "Rosalia", "Selina", "Sharlene", "Sierra", "Sydney", "Terra", "Tori", "Vonda", "Zelda",
              "Mohamed", "Youssef", "Ahmed", "Mahmoud", "Mustafa", "Taha", "Hamza", "Ibrahim", "Hassan", "Hussein", "Karim", "Tareq", "Abdel-Rahman", "Ali", "Omar", "Halim", "Murad", "Selim", "Abdallah", "Peter", "Pierre", "George", "John", "Mi",
              "Kirollos", "Mark", "Habib", "Manuel", "Juan", "Antonio", "Mohammed", "Ahmed", "Ali", "Hamza", "Ibrahim", "Mahmoud", "Abdallah", "Tareq", "Hassan", "Khaled", "Mamadou", "Moussa", "Mahamadou", "Adama", "Bakary", "Abdoulaye", "Modibo",
              "Oumar", "Sekou", "Souleymane", "Mohamed", "Ahmed", "Mohammed", "Said", "Rachid", "Mustapha", "Youssef", "Hassan", "Abdel-salam", "Ali", "Mehdi", "Youssef", "Aziz", "Karim", "Fatima", "Sara", "Fatiha", "Aicha", "Fatma", "Ami", "Meriem",
              "Karima", "Kheira", "dia", "Shaimaa", "Fatma", "Reem", "Farida", "Aya", "Shahd", "Ashraqat", "Sahar", "Fatin", "Dalal", "Suha", "Rowan", "Habiba", "Mary", "Marie", "Mariam", "Mari", "Irene", "Malak", "Ha", "Farah", "Marwa", "Salma",
              "Carmen", "Isabel", "Teresa", "Esperanza", "Milagrosa", "Aya", "Rania", "Sarah", "Reem", "Hoda", "Marwa", "Mo", "Fatima", "Eisha", "Nesreen", "Fatoumata", "Mariam", "Amita", "Hawa", "Awa", "Oumou", "Djeneba", "Bintou", "Fanta",
              "Kadiatou", "Fatima", "Khadija", "Aicha", "Malika", "Hima", "Rachida", "dia", "Karima", "Ami", "Saida", "Mariam", "Shayma", "Khawla", "Juan", "Santiago", "Thiago", "Lucas", "Santino", "Lautaro", "Ian", "Mateo", "Daniel", "Dylan", "Dyllan",
              "Kevin", "Keven", "Miguel", "Davi", "Arthur", "Gabriel", "Pedro", "Lucas", "Matheus", "Berrdo", "Rafael", "Guilherme", "William", "Jacob", "Liam", "than", "Noah", "Ethan", "Lucas", "Lukas", "Benjamin", "Samuel", "Logan", "Liam", "Ethan", "Jacob",
              "Logan", "Mason", "Benjamin", "Lucas", "Alexander", "Carter", "Noah", "Ethan", "Liam", "Lucas", "Mason", "Logan", "Noah", "Alexander", "Benjamin", "Jacob", "Jack", "Liam", "Mason", "Carter", "Noah", "Logan", "Lucas", "William", "Benjamin",
              "Jacob", "Hunter", "Jacob", "Ethan", "Benjamin", "Lucas", "Owen", "Noah", "Mason", "Carter", "Hunter", "Liam", "Ethan", "Jacob", "Lucas", "Benjamin", "Liam", "Hunter", "Connor", "Jack", "Cohen", "Jaxon", "John", "Landon", "Owen",
              "William", "Benjamin", "Caleb", "Henry", "Lucas", "Mason", "Noah", "Alex", "Alexander", "Carter", "Charlie", "David", "Jackson", "James", "Jase", "Joseph", "Wyatt", "Austin", "Camden", "Cameron", "Emmett", "Griffin", "Harrison", "Hudson",
              "Jace", "Joh", "Kingston", "Lincoln", "Marcus", "Sha", "Than", "Oliver", "Parker", "Ryan", "Ryder", "Seth", "Xavier", "Charles", "Clark", "Cooper", "Daniel", "Drake", "Dylan", "Edward", "Eli", "Elijah", "Emerson", "Evan", "Felix", "Gabriel",
              "Gavin", "Gus", "Isaac", "Isaiah", "Jacob", "Jax", "Kai", "Kaiden", "Michael", "Thaniel", "Riley", "Thomas", "Tristan", "Antonio", "Beau", "Beckett", "Brayden", "Bryce", "Caden", "Casey", "Cash", "Chase", "Clarke", "Dawson", "Declan",
              "Dominic", "Drew", "Elliot", "Elliott", "Ethan", "Ezra", "Gage", "Grayson", "Hayden", "Jaxson", "Jayden", "Kole", "Levi", "Logan", "Luke", "Matthew", "Morgan", "te", "Nolan", "Peter", "Sebastian", "Simon", "Tanner", "Taylor", "Theo",
              "Turner", "William", "than", "Olivier", "Alexis", "Samuel", "Gabriel", "Thomas", "Jacob", "Liam", "Carter", "Noah", "Lucas", "Ethan", "Jacob", "Mason", "Owen", "William", "Jace", "Alexander", "Jaxon", "Bentley", "Alma", "Isabella", "Zoe",
              "Catali", "Camila", "Alysha", "Isabella", "Isabelle", "Emily", "Emely", "Sophia", "Julia", "Alice", "Manuela", "Isabella", "Laura", "Maria", "Eduarda", "Giovan", "Valenti", "Beatriz", "Maya", "Mia", "Mya", "Sofia", "Sophia", "Olivia", "Emma", "Emily",
              "Chloe", "Khloe", "Ava", "Isabella", "Isobella", "Sara", "Sarah", "Lea", "Leah", "Emma", "Olivia", "Emily", "Sophia", "Ava", "Lily", "Ella", "Isabella", "Abigail", "Chloe", "Olivia", "Emma", "Sophia", "Emily", "Ava", "Ella", "Chloe", "Isabella",
              "Avery", "Hanh", "Emily", "Emma", "Olivia", "Sophia", "Ava", "Lily", "Chloe", "Avery", "Abigail", "Haley", "Olivia", "Emma", "Lily", "Sophia", "Ava", "Sophie", "Emily", "Abigail", "Chloe", "Isabella", "Olivia", "Emma", "Sophia", "Ava",
              "Brooklyn", "Olivia", "Ellie", "Madison", "Claire", "Ella", "Emma", "Lydia", "Sophia", "Alexis", "Julia", "Lauren", "Mackenzie", "Sophie", "Abigail", "Amelia", "Ava", "Charlotte", "Layla", "Lily", "Sadie", "Summer", "Victoria", "Alexa",
              "An", "Annie", "Aria", "Aubree", "Danica", "Elizabeth", "Felicity", "Grace", "Hanh", "Harper", "Jessica", "Jordyn", "Keira", "Lexi", "Madelyn", "Molly", "Mya", "Peyton", "Piper", "Quinn", "Sarah", "Scarlett", "Stella", "Tessa", "Violet",
              "Aaralyn", "Adalyn", "Alice", "Alyson", "Amy", "Abelle", "Averie", "Avery", "Ayla", "Brooke", "Brooklynn", "Casey", "Charlie", "Emersyn", "Evelyn", "Fio", "Georgia", "Gracie", "Hailey", "Isabella", "Isla", "Izabella", "Jaelyn", "Kate",
              "Katherine", "Kathryn", "Kayla", "Kyleigh", "Leah", "Lylah", "Macie", "Maggie", "Mary", "Meredith", "Mila", "Nevaeh", "Paige", "Rebekah", "Ruby", "Ryleigh", "Samantha", "Savanh", "Sere", "Taylor", "Zoey", "Emma", "Olivia",
              "Florence", "Alice", "Wei", "Yong", "Wen", "Wei", "Jie", "Hao", "Yi", "Jun", "Feng", "Yong", "Jian", "Bin", "Lei", "Aarav", "Vivaan", "Aditya", "Vihaan", "Arjun", "Reyansh", "Muhammad", "Sai", "Arv", "Ayaan",
              "Aarav", "Aaryan", "Abhiv", "Arv", "Devansh", "Dhruv", "Ishan", "Prav", "Shaurya", "Tejas", "Amir", "Ali", "AbulFazl", "Amir", "Hossein", "Ali", "Mohammad", "Amir", "Mohammad", "Mahdi", "Hossein", "Mohammad-Mahdi", "Mohammad", "Reza",
              "Mohammad", "Ali", "Hossein", "Mahdi", "Hassan", "Reza", "Ahmad", "Mohammad", "Reza", "Abbas", "Ali-Reza", "Ali", "Muhammed", "Hussein", "Hydar", "Ahmed", "Omar", "Hasan", "Kathem", "Abdullah", "Ammar", "Noam", "Uri", "Itai", "Yosef",
              "David", "Yehotan", "Daniel", "Ariel", "Moshe", "Eitan", "Noam", "Amit", "Ariel", "Daniel", "Adi", "Ma'ayan", "Yuval", "Yahli", "Omer", "Lior", "Mohammad", "Ahmad", "Mahmed", "Yusuf", "Abed", "Adam", "Omar", "Ali", "Mahmoud", "Amir",
              "George", "Elias", "Majd", "Daniel", "Yusuf", "Ha", "Julian", "Charbel", "Jude", "Amir", "Adam", "Omri", "Eyal", "Amir", "Salman", "Rani", "Tamir", "Yosef", "Bahah", "Daniel", "Hiroto", "Ren", "Yuuma", "Mito", "Haruto", "Shota", "Yuuto",
              "Haruto", "Souma", "Sota", "Mohammad", "Ahmad", "Abdul", "Rahman", "Muhamad", "Ahmad", "Adam", "Aqil", "Aryan", "Yusuf", "Putera", "Mikhail", "Emir", "Ariff", "ranbaatar", "Batukhan", "Bataar", "Chuluun", "Sukhbataar", "Mohammad", "Ali",
              "Hussain", "Omar", "Bilal", "Usman", "Zahid", "Shahid", "Saqib", "Nomaan", "John", "Paul", "Justin", "Renz", "Clarence", "John", "Carl", "Kevin", "Richard", "Ezekiel", "Jared", "Xyriel", "Min-jun", "Ji-hu", "Ji-hoon", "Jun-seo", "Hyun-woo",
              "Ye-jun", "Kun-woo", "Hyun-jun", "Min-jae", "Woo-jin", "Chia-hao", "Chih-ming", "Chun-chieh", "Chien-hung", "Chun-hung", "Muhammad", "Yusuf", "Abdullo", "Abubakr", "Somchai", "Somsak", "Somporn", "Somboon", "Prasert", "Yusuf", "Mustafa",
              "Berat", "Emir", "Mehmet", "Ahmet", "Muhammed", "Enes", "A-mer", "Emirhan", "Mohammad", "Abdullah", "Ahmed", "Ali", "Khalid", "Saeed", "Omar", "Rashid", "Maryam", "Zhen", "Jing", "Ying", "Yan", "Li", "Xiaoyan", "Xinyi", "Jie", "Lili",
              "Xiaomei", "Tingting", "Saanvi", "Aanya", "Aadhya", "Aaradhya", "Anya", "Pari", "Anika", "Vya", "Angel", "Diya", "Anya", "Anika", "Aradhya", "Harini", "Avya", "Ridhi", "Rishika", "Sanvi", "Shreya", "Trisha", "Fatemeh", "Zahra", "Setayesh",
              "Hasti", "Zeib", "zanin-Zahra", "Reihaneh", "Maryam", "Mobi", "Fatemeh", "Zahra", "Maryam", "Ma'soumeh", "Sakineh", "Zeib", "Roghayyeh", "Khadije", "Leyla", "Somayyeh", "Noa", "Shira", "Tamar", "Talia", "Maya", "Yael", "Sarah", "Adele",
              "Ayala", "Michal", "Noam", "Amit", "Ariel", "Daniel", "Adi", "Ma'ayan", "Yuval", "Yahli", "Omer", "Lior", "Maryam", "Rahaf", "Leen", "Lian", "Rimas", "Hala", "Noor", "Bisan", "Malk", "Aya", "Maria", "Celine", "Aline", "Maya", "Noor",
              "Lian", "Maryam", "talie", "Tala", "Miral", "Eden", "Yarin", "Nur", "Sarah", "Sillin", "Assil", "Malk", "Maya", "Aya", "Miyar", "Yui", "Hi", "Aoi", "Yua", "Yui", "Rin", "Airi", "Koharu", "Airi", "Mei", "Rimas", "Ja", "Hala", "Nor",
              "Puteri", "Siti", "Aishah", "Sara", "Sophia", "Nurin", "Rania", "Hanh", "Khayla", "Odval", "Bolormaa", "Bayarmaa", "Oyunbileg", "Khongordzol", "Fatima", "Fozia", "Sadia", "Sobia", "dia", "Maryam", "Farza", "Ayesha", "Sakee", "Zaib",
              "Althea", "Jessa Mae", "Rhea Mae", "Mary Rose", "Kyla", "April Joy", "Jane", "Alexandra", "Precious", "Althea Mae", "Seo-yeon", "Min-seo", "Seo-hyeon", "Ji-woo", "Seo-yun", "Ji-min", "Su-bin", "Ha-eun", "Ye-eun", "Yun-seo", "Shu-fen",
              "Shu-hui", "Mei-ling", "Ya-ting", "Mei-hui", "Sumayah", "Asiya", "Oisha", "Googoosh", "Anohito", "Indira", "Zeynep", "Elif", "Ecrin", "Dave", "Aard")

#from wikipedia and some rpg class list
properTitles = ("Emperor", "Empress", "King", "Queen", "Viceroy", "Vicereine", "Prince", "Princess", "Duke", "Duchess", "Count", "Countess", "Baron", "Baroness", "Pope", "Viscount", "Viscountess", "Earl", "Marquis", "Marquess", "Archon", "Tsar",
                "Tsarina", "Representative", "Senator", "Speaker", "President", "Councillor", "Alderman", "Delegate", "Mayor", "Mayoress", "Governor", "Governess", "Prefect", "Prelate", "Premier", "Burgess", "Ambassador", "Envoy", "Secretary",
                "Minister", "Attach", "Provost", "Advocate", "Attorney", "Bailiff", "Barrister", "Chancellor", "Judge", "Justice", "Magistrate", "Promagistrate", "Chairman", "Mufti", "Solicitor", "Lictor", "Reeve", "Seneschal", "Tribune",
                "Abbess", "Abbot", "Brother", "Sister", "Friar", "Mother", "Father", "Bishop", "Presbyter", "Priest", "Sheperd", "Patriarch", "Pope", "Catholicos", "Vicar", "Chaplain", "Canon", "Pastor", "Prelate", "Dom", "Cardinal", "Ter", "Coach",
                "Venerable", "Blessed", "Saint", "Messiah", "Deacon", "Archdeacon", "Acolyte", "Dean", "Elder", "Minister", "Monsignor", "Reader", "Almoner", "Colonel", "General", "Commodore", "Corporal", "Sergeant", "Admiral", "Brigadier",
                "Captain", "Commander", "General", "Officer", "Lieutenant", "Major", "Vicar", "Private", "Constable", "Agent", "Principal", "Comrade", "Dictator",
                "Fighter", "Barbarian", "Knight", "Swashbuckler", "Paladin", "Dark Knight", "Dragon Knight", "Samurai", "Warlord", "Hero", "Magician", "Inherent Gift Magician", "Theurgist Magician", "Summoner Magician", "Vancian Magician",
                "Red Mage:", "Blue Mage:", "Necromantic Magician", "Illusionist Magician", "Nature Magician", "Elemental Magician", "Druid Magician", "Shamanic Magician", "Elemental Magician", "Rogue", "Thief", "Assassin", "Gambler", "Ninja",
                "Shadow", "Pirate", "Scout", "Cleric", "Priest", "Battle Priest", "Witch Doctor", "Templar", "Caster", "Ranger", "Sniper Ranger", "Bow and Blade Ranger", "Beastmaster Ranger", "Dual Wielding Ranger", "Trapper Ranger",
                "Magical Ranger", "Magic Knight", "Bard", "Dancer", "Monk", "Engineer", "Alchemist", "Psychic", "Gunslinger","Brute"
                "Arch", "Grand", "Prime", "Head", "Lord", "Chief", "Superior", "High", "Supreme")

#from myvocabulary.com
adjectives = ("Able", "Abundant", "Accepting", "Accommodating", "Active", "Addictive", "Adequate", "Aggressive", "Amazing", "Amiable", "Amicable", "Amusing", "Antagonistic", "Anxious", "Anxious", "Apathetic", "Aquatic", "Arrogant", "Articulate",
              "Artistic", "Attentive", "Attractive", "Authoritative", "Awesome", "Barren", "Benevolent", "Biodegradable", "Blase", "Bold", "Bonding", "Boorish", "Bountiful", "Braggart", "Brave", "Brilliant", "Buoyant", "Busy", "Buzzing", "Callow",
              "Captious", "Caring", "Celestial", "Charming", "Chaste", "Cheating", "Cheerful", "Churlish", "Civil", "Clean", "Clever", "Cold", "Colossal", "Combustible", "Comfortable", "Commercial", "Communicative", "Compact", "Competitive",
              "Compulsive", "Confident", "Conflicted", "Congenial", "Conscientious", "Conservative", "Considerate", "Conspicuous", "Contemptible", "Contiguous", "Cooperative", "Cordial", "Courageous", "Courteous", "Covetous", "Creative", "Critical",
              "Critical", "Crucial", "Crude", "Curious", "Current", "Curt", "Cynical", "Decent", "Decorous", "Defensive", "Deferential", "Deft", "Dejected", "Delightful", "Demeaning", "Demise", "Dependable", "Deplorable", "Depressed",
              "Destructive", "Devious", "Devoted", "Dictatorial", "Diligent", "Diminutive", "Diplomatic", "Discreet", "Disdainful", "Dishonesty", "Dishonorable", "Disposable", "Disrespectful", "Distracted", "Docile", "Downcast", "Dynamic", "Dynamic",
              "Earnest", "Earthy", "Ecological", "Efficient", "Egotistical", "Electrifying", "Elitist", "Empathetic", "Endangered", "Endemic", "Energetic", "Enigmatic", "Enthusiastic", "Esteemed", "Estimable", "Ethical", "Euphoric", "Evergreen",
              "Exclusive", "Expectant", "Explosive", "Exquisite", "Extravagant", "Extrovert", "Exuberant", "Fair", "Faithful", "Fallow", "Falseness", "Famous", "Fancy", "Ferocious", "Fertile", "Fervent", "Fervid", "Fibrous", "Fierce", "Flexible",
              "Focused", "Forgiving", "Forlorn", "Frail", "Generous", "Genial", "Genteel", "Gentle", "Genuine", "Gifted", "Gigantic", "Glib", "Gloomy", "Good", "Gorgeous", "Grace", "Gracious", "Grand", "Grateful", "Grabby", "Grouchy",
              "Guilty", "Guilty", "Gusty", "Happy", "Hard-hearted", "Healing", "Heedless", "Helpfulness", "Heroic", "Honest", "Honorable", "Hopeful", "Hostile", "Humane", "Humble", "Humorous", "Hygienic", "Hysterical", "Idealistic", "Idolize",
              "Ignoble", "Ignorant", "Ill-tempered", "Impartial", "Impolite", "Improper", "Imprudent", "Impudent", "Indecent", "Indecorous", "Indifference", "Indigenous", "Industrious", "Ingenuous", "Innocent", "Innovative", "Insightful", "Insolent",
              "Inspirational", "Instructive", "Insulting", "Intense", "Intense", "Intense", "Intolerant", "Introvert", "Intuitive", "Inventive", "Investigative", "Irresponsible", "Jaundiced", "Jealous", "Jealous", "Jocular", "Jolly",
              "Jovial", "Joyful", "Jubilant", "Just", "Juvenile", "Keen", "Kind", "Kindred", "Knowledgeable", "Liberal", "Listener", "Loathsome", "Loving", "Loyal", "Magical", "Magnificent", "Malevolent", "Malicious", "Mammoth",
              "Manipulative", "Marine", "Mastery", "Meddling", "Meritorious", "Meticulous", "Migratory", "Minuscule", "Miserable", "Mistrustful", "Modest", "Moral", "Mysterious", "Naive", "Nascent", "Native", "Natural", "Natural", "Nature", "Needy",
              "Nefarious", "Negative", "Neglected", "Neglectful", "Negligent", "Nice", "Noble", "Notorious", "Obedient", "Observant", "Open", "Open-minded", "Opinionated", "Oppressive", "Orderly", "Oriented", "Original", "Outrageous", "Outspoken",
              "Parasitic", "Partial", "Passionate", "Patient", "Perceptive", "Personable", "Personal", "Petulant", "Pleasant", "Poise", "Polite", "Pollutant", "Popular", "Popular", "Powerful", "Prejudicial", "Preposterous", "Pretentious", "Prideful",
              "Principled", "Pristine", "Prompt", "Proper", "Punctual", "Purposeful", "Quaint", "Quarrelsome", "Quick", "Quiet", "Quiet", "Quirky", "Radioactive", "Rancorous", "Rational", "Reasonable", "Reckless", "Refined", "Reflective", "Reliant",
              "Remarkable", "Remorseful", "Repugnant", "Resilient", "Resilient", "Resolute", "Resourceful", "Respectful", "Responsible", "Responsive", "Restorative", "Reverent", "Rotting", "Rude", "Ruthless", "Sad",
              "Safe", "Scornful", "Scrumptious", "Selfish", "Sensible", "Sensitive", "Simple", "Sober", "Solar", "Solemn", "Solitary", "Sour", "Spatial", "Special", "Splendid", "Splendid", "Staunch", "Staunch", "Stern", "Stunning",
              "Successful", "Sullen", "Superb", "Superior", "Supportive", "Surly", "Suspicious", "Sweet", "Sympathetic", "Tactful", "Taint", "Temperate", "Temperate", "Tenacious", "Terrific", "Testy", "Thoughtful", "Thoughtless", "Tolerant", "Towering",
              "Toxic", "Treacherous", "Tropical", "Trustworthy", "Truthful", "Ultimate", "Ultimate", "Uncivil", "Uncouth", "Undeveloped", "Unethical", "Unfair", "Unique", "Unique", "Unmannerly", "Unrefined", "Unsavory", "Unworthy",
              "Uplifting", "Upright", "Uproot", "Upstanding", "Valiant", "Veracious", "Versatile", "Vicious", "Vigilant", "Vigilant", "Vigorous", "Vile", "Villainous", "Virtuous", "Visible", "Visible", "Vivacious", "Vocal", "Volatile", "Volunteering",
              "Vulnerable", "Warm", "Wary", "Waspish", "Watchful", "Welcoming", "Wicked", "Wild", "Willing", "Winning", "Winsome", "Wise", "Wishy-washy", "Wistful", "Witty", "Woeful", "Wonderful", "Worried", "Worthwhile", "Worthy")

lesser = ("Assistant", "Aide", "Lieutenant", "Sergent", "Hand", "Envoy", "Chosen", "Protege", "Helper", "Attendant", "Squire", "Page", "Trainee", "Padawan", "Vice")

#wikipedia
countryNames = ["Abkhazia", "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua", "and", "Barbuda", "Argentina", "Armenia", "Australia", "Austria", "Azerbaijan", "Bahamas,", "The", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", 
    "Belize", "Benin", "Bhutan", "Bolivia", "Bosnia", "and", "Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria", "Burkina", "Faso", "Burma", "Burundi", "Cambodia", "Cameroon", "Canada", "Cape", "Verde", "Central", "African", "Republic", "Chad", 
    "Chile", "China", "Taiwan", "Colombia", "Comoros", "Congo,", "Democratic", "Republic", "of", "the", "Congo,", "Republic", "of", "the", "Cook", "Islands", "Costa", "Rica", "Ivory", "Coast", "Croatia", "Cuba", "Cyprus", "Czech", "Republic", "Korea,", 
    "North", "Congo,", "Democratic", "Republic", "of", "the", "Denmark", "Djibouti", "Dominica", "Dominican", "Republic", "East", "Timor", "Ecuador", "Egypt", "El", "Salvador", "Equatorial", "Guinea", "Eritrea", "Estonia", "Ethiopia", "Fiji", "Finland", 
    "France", "Gabon", "Gambia,", "The", "Georgia", "Germany", "Ghana", "Greece", "Grenada", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Vatican", "City", "Honduras", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland", 
    "Israel", "Italy", "Ivory", "Coast", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Korea,", "North", "Korea,", "South", "Kosovo", "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", 
    "Lithuania", "Luxembourg", "Macedonia", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall", "Islands", "Mauritania", "Mauritius", "Mexico", "Micronesia,", "Federated", "States", "of", "Moldova", "Monaco", "Mongolia", "Montenegro", 
    "Morocco", "Mozambique", "Burma", "Nagorno-Karabakh", "Namibia", "Nauru", "Nepal", "Netherlands", "New", "Zealand", "Nicaragua", "Niger", "Nigeria", "Niue", "Northern", "Cyprus", "Korea,", "North", "Norway", "Oman", "Pakistan", "Palau", "Palestine", 
    "Panama", "Papua", "New", "Guinea", "Paraguay", "Peru", "Philippines", "Poland", "Portugal", "Transnistria", "Qatar", "Korea,", "South", "Congo,", "Republic", "of", "the", "Romania", "Russia", "Rwanda", "Sahrawi", "Arab", "Democratic", "Republic", "Saint", 
    "Kitts", "and", "Nevis", "Saint", "Lucia", "Saint", "Vincent", "and", "the", "Grenadines", "Samoa", "San", "Marino", "Sao", "Tome", "and", "Principe", "Saudi", "Arabia", "Senegal", "Serbia", "Seychelles", "Sierra", "Leone", "Singapore", "Slovakia", "Slovenia", "Solomon", "Islands", "Somalia", "Somaliland", "South", "Africa", "Korea,", "South", "South", "Ossetia", "South", "Sudan", "Spain", "Sri", "Lanka", "Sudan", "South", "Sudan", "Suriname", "Swaziland", "Sweden", "Switzerland", "Syria", "Taiwan", "Tajikistan", "Tanzania", "Thailand", "East", "Timor", "Togo", "Tonga", "Transnistria", "Trinidad", "and", "Tobago", "Tunisia", "Turkey", "Turkmenistan", "Tuvalu", "Uganda", "Ukraine", "United", "Arab", "Emirates", "United", "Kingdom", "United", "States", "Uruguay", "Uzbekistan", "Vanuatu", "Vatican", "City", "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe", "Abkhazia", "Cook", "Islands", "Kosovo", "Niue", "Northern", "Cyprus", "Sahrawi", "Arab", "Democratic", "Republic", "Somaliland", "South", "South", "North", "East", "West", "Ossetia", "Taiwan", "Transnistria"
    "New York", "Los Angeles", "Chicago", "Houston", "Philadelphia", "Phoenix", "San Antonio", "San Diego", "Dallas", "San Jose", "Austin", "Jacksonville", "Indianapolis", "San Francisco", "Columbus", "Fort Worth", "Charlotte", "Detroit", "El Paso", "Memphis", "Boston", "Seattle", "Denver", "Washington", "Nashville", "Baltimore", "Louisville", "Portland", "Oklahoma City", "Milwaukee", "Las Vegas", "Albuquerque", "Tucson", "Fresno", "Sacramento", "Long Beach", "Kansas City", "Mesa", "Virginia Beach", "Atlanta", "Colorado Springs", "Raleigh", "Omaha", "Miami", "Oakland", "Tulsa", "Minneapolis", "Cleveland", "Wichita", "Arlington", "New Orleans", "Bakersfield", "Tampa", "Honolulu", "Anaheim", "Aurora", "Santa Ana", "St. Louis", "Riverside", "Corpus Christi", "Pittsburgh", "Lexington", "Anchorage", "Stockton", "Cincinnati", "Saint Paul", "Toledo", "Newark", "Greensboro", "Plano", "Henderson", "Lincoln", "Buffalo", "Fort Wayne", "Jersey City", "Chula Vista", "Orlando", "St. Petersburg", "Norfolk", "Chandler", "Laredo", "Madison", "Durham", "Lubbock", "Winston–Salem", "Garland", "Glendale", "Hialeah", "Reno", "Baton Rouge", "Irvine", "Chesapeake", "Irving", "Scottsdale", "North Las Vegas", "Fremont", "Gilbert", "San Bernardino", "Boise", "Birmingham", "Rochester", "Richmond", "Spokane", "Des Moines", "Montgomery", "Modesto", "Fayetteville", "Tacoma", "Shreveport", "Fontana", "Oxnard", "Aurora", "Moreno Valley", "Akron", "Yonkers", "Columbus", "Augusta", "Little Rock", "Amarillo", "Mobile", "Huntington Beach", "Glendale", "Grand Rapids", "Salt Lake City", "Tallahassee", "Huntsville", "Worcester", "Knoxville", "Grand Prairie", "Newport News", "Brownsville", "Santa Clarita", "Overland Park", "Providence", "Jackson", "Garden Grove", "Oceanside", "Chattanooga", "Fort Lauderdale", "Rancho Cucamonga", "Santa Rosa", "Port St. Lucie", "Ontario", "Tempe", "Vancouver", "Springfield", "Cape Coral", "Pembroke Pines", "Sioux Falls", "Peoria", "Lancaster", "Elk Grove", "Corona", "Eugene", "Salem", "Palmdale", "Salinas", "Springfield", "Pasadena", "Rockford", "Pomona", "Hayward", "Fort Collins", "Joliet", "Escondido", "Kansas City", "Torrance", "Bridgeport", "Alexandria", "Sunnyvale", "Cary", "Lakewood", "Hollywood", "Paterson", "Syracuse", "Naperville", "McKinney", "Mesquite", "Clarksville", "Savannah", "Dayton", "Orange", "Fullerton", "Pasadena", "Hampton", "McAllen", "Killeen", "Warren", "West Valley City", "Columbia", "New Haven", "Sterling Heights", "Olathe", "Miramar", "Thousand Oaks", "Frisco", "Cedar Rapids", "Topeka", "Visalia", "Waco", "Elizabeth", "Bellevue", "Gainesville", "Simi Valley", "Charleston", "Carrollton", "Coral Springs", "Stamford", "Hartford", "Concord", "Roseville", "Thornton", "Kent", "Lafayette", "Surprise", "Denton", "Victorville", "Evansville", "Midland", "Santa Clara", "Athens", "Allentown", "Abilene", "Beaumont", "Vallejo", "Independence", "Springfield", "Ann Arbor", "Provo", "Peoria", "Norman", "Berkeley", "El Monte", "Murfreesboro", "Lansing", "Columbia", "Downey", "Costa Mesa", "Inglewood", "Miami Gardens", "Manchester", "Elgin", "Wilmington", "Waterbury", "Fargo", "Arvada", "Carlsbad", "Westminster", "Rochester", "Gresham", "Clearwater", "Lowell", "West Jordan", "Pueblo", "San Buenaventura (Ventura)", "Fairfield", "West Covina", "Billings", "Murrieta", "High Point", 
    "Round Rock", "Richmond", "Cambridge", "Norwalk", "Odessa", "Antioch", "Temecula", "Green Bay", "Everett", "Wichita Falls", "Burbank", "Palm Bay", "Centennial", "Daly City", "Richardson", "Pompano Beach", "Broken Arrow", "North Charleston", "West Palm Beach", "Boulder", "Rialto", "Santa Maria", "El Cajon", "Davenport", "Erie", "Las Cruces", "South Bend", "Flint", "Kenosha",
    "London", "Berlin", "Madrid", "Rome", "Paris", "Bucharest", "Vienna", "Hamburg", "Budapest", "Warsaw", "Barcelona", "Milan", "Munich", "Prague", "Sofia", "Brussels", "Birmingham", "Cologne", "Naples", "Turin", "Stockholm", "Marseille", "Amsterdam", "Valencia", "Zagreb", "Krakow", "Leeds", "Lodz", "Seville", "Frankfurt", "Zaragoza", "Riga", "Athens", "Palermo", "Wroclaw", "Rotterdam", "Genoa", "Helsinki", "Stuttgart", "Glasgow", "Dusseldorf", "Dortmund", "Mcalaga", "Essen", "Copenhagen", "Sheffield", "Poznan", "Lisbon", "Bremen", "Vilnius", "Gothenburg", "Dresden", "Dublin", "Bradford", "Leipzig", "Antwerp", "Manchester", "Hannover", "The_Hague", "Edinburgh", "Nuremberg", "Duisburg", "Lyon", "Liverpool", "Gdansk", "Toulouse", "Murcia", "Bristol", "Tallinn", "Bratislava", "Szczecin", "Palma de Mallorca", "Bologna", "Las Palmas de Gran Canaria", "Florence", "Brno", "Bydgoszcz", "Bochum", "Bilbao", "Cardiff", "Lublin", "Nice", "Wuppertal", "Plovdiv", "Varna", "Alicante", "Leicester", "Córdoba", "Bielefeld", "City of Wakefield", "Thessaloniki", "Utrecht", "Metropolitan Borough of Wirral", "Aarhus", "Bari", "Coventry", "Valladolid", "Bonn", "Cluj", "Napoca", "Malmö", "Nottingham", "Katowice", "Kaunas", "Timisoara",
    "San", "Pan", "Narnia", "Moria", "Shire", "Tamriel"]
countrySylables = []

#minecraft+my own spin
areaBiome = ["Taiga", "Plain", "River", "Beach", "Hill", "Mountain", "Island", "Cliff", "Headland", "Moor", "Highland", "Desert", "Forest", "Jungle", "Swamp", "Savannah", "Mesa", "Plateau", "Ocean", "Wasteland", "Valley", "Chasm", "Abyss", "Waterfall", 
    "Town", "Village", "City", "Alley", "Slum", "Homestead", "Cabin", "Camp", "Road", "Highway", "Tower", "Citadel", "Compound", "Complex", "Keep", "Dungeon", "Castle", "Crypt", "Cellar", "Tomb", "Ruin", "Fortress", 
    "Great Hall", "Town Center", "Monastary", "Church", "Cathedrel", "Temple", "Coast", "Port"]

#minecraft+my own spin
areaAdj = ["Snowy", "Frozen", "Cold", "Flamed", "Hot", "Rainy", "Stormy", "Mega", "Great", "Holy", "Unholy", "Spruce", "Stone", "Deep", "Foul", "Withered", "Courrupted", "Dark", "Bright", "Stunning", "Sunken", "Watery", "Slimey", "Oozing"]


def flatten(l, limit=1000, counter=0):
  for i in xrange(len(l)):
    if (isinstance(l[i], (list, tuple)) and
        counter < limit):
      for a in l.pop(i):
        l.insert(i, a)
        i += 1
      counter += 1
      return flatten(l, limit, counter)
  return l

def break_string(string, letterType):

    if(len(string)<6):
        return string

    listSyla = []

    listOfIndecies= [letterType.find("VCC"),letterType.find("CVC"),letterType.find("VVC"),letterType.find("CCC")]
    if(listOfIndecies[0] < 3 ):
        listOfIndecies[0] = letterType[2:].find("VCC")+2

    if(listOfIndecies[1] < 3 ):
        listOfIndecies[1] = letterType[2:].find("CVC")+2

    if(listOfIndecies[2] < 3 ):
        listOfIndecies[2] = letterType[2:].find("VVC")+2

    if(listOfIndecies[3] < 3 ):
        listOfIndecies[3] = letterType[2:].find("CCC")+2

    for i in listOfIndecies:

        if(i > 1 and i + 2 < len(string)):

            listSyla.append(break_string(string[:i+1],letterType[:i+1]))
            listSyla.append(break_string(string[i+1:],letterType[i+1:]))

    if(listSyla == []):
        return string

    return listSyla
        


def split_by_syllable(stringList=("")):

    newList = []

    for current in stringList:

        split = current.split()

        for curr in split:
            split2 = curr.split("–")

            for curr in split2:

                newList.append(curr.lower().translate(None,',.-_%0123456789'))

    vowel = ['a','e','i','o','u','y']
    const = ['q','w','r','t','p','s','d','f','g','h','j','k','l','z','x','c','v','b','n','m']
    typeList = copy.deepcopy(newList)

    for i in range(0,len(newList)):

        for v in vowel:
            typeList[i] = typeList[i].replace(v,"V")

        for c in const:
            typeList[i] = typeList[i].replace(c,"C")


    listSyla = []

    for i in range(0,len(newList)):

        listSyla.append(break_string(newList[i],typeList[i]))

    listSyla = flatten(listSyla)

    return listSyla


def item():

    return itemEffect[random.randint(0,len(itemEffect)-1)]+" "+qualityType[random.randint(0,len(qualityType)-1)]+" "+materialType[random.randint(0,len(materialType)-1)]+" "+itemType[random.randint(0,len(itemType)-1)]


def name_assist(titleVar, title, adj, name):

    if(random.random() < 0.3):
        title2 = title+random.randint(1,titleVar)
        if(random.random()<0.5):
            title2 = -title2
            
        string = name+"'s "+lesser[random.randint(0,len(lesser)-1)]+" "+properTitles[title2]+", "+firstNames[random.randint(0,len(firstNames)-1)]
    
    else:
        if(random.random() < 0.5):
            adj += random.randint(1,5)
        else:
            adj -= random.randint(1,5)
            
        string = name+"'s "+adjectives[adj]+" "+lesser[random.randint(0,len(lesser)-1)]+", "+firstNames[random.randint(0,len(firstNames)-1)]
    
    return string


def name():
    titleVar = 4;
    title = random.randint(titleVar,len(properTitles)-1-titleVar)
    adj = random.randint(5,len(adjectives)-6)

    string = firstNames[random.randint(0,len(firstNames)-1)]+" the "+adjectives[adj]+" "+properTitles[title]#+" "+properTitles[random.randint(title-10,title+10)]
    #string += "\n\tcarrying the: "+item()
    #string += "\n\t              "+item()
    string += "\n    "+name_assist(titleVar, title, adj, string.partition(' ')[0])
    #string += "\n\tcarrying the: "+item()
    string += "\n    "+name_assist(titleVar, title, adj, string.partition(' ')[0])
    #string += "\n\tcarrying the: "+item()
    string += "\n"
    
    return string


def area_name(length=4, startingLetter=None):

    def syl():
        return countrySylables[random.randint(0,len(countrySylables)-1)].lower()

    name = syl()
    while(len(name)<length):
        name += syl()

    # set up the vowel and constonant status
    vowel = ['a','e','i','o','u','y']
    const = ['q','w','r','t','p','s','d','f','g','h','j','k','l','z','x','c','v','b','n','m']
    typeString = name
    for v in vowel:
        typeString = typeString.replace(v,"V")
    for c in const:
        typeString = typeString.replace(c,"C")

    #early failure
    #optional 2-character bad combos: "rc","rs","rk","nd","tb","nb","mb","pz","rl","rf","lt","ld","nt","mh","gf",
    badCombos = ["pmb","ngf","fkt","crm","vns","vms"]
    for c in badCombos:
        if(name.find(c) >= 0):
            return area_name(length)

    if(typeString.find("CCCC") >= 0 or typeString.count("C") > typeString.count("V")*4 or typeString.count("C") <= typeString.count("V") or name[0] == name[1]):
        return area_name(length)

    if(typeString[:3]=="CCC"):
        typeString = typeString[2:]
        name = name[2:]

    if(typeString[:2]=="CC"):
        typeString = typeString[1:]
        name = name[1:]

    if(len(name)<length):
        return area_name(length)

    return name.title()

def descriptive_area(length=6):

    name = areaAdj[random.randint(0,len(areaAdj)-1)]
    name += " " + areaBiome[random.randint(0,len(areaBiome)-1)]
    name += " of " + area_name(length)

    return name

#do not call, is broken
def drawMain():

    segment_length = (50,100)
    surface = pygame.surface()
    shape_center = (150,150)
    shape_variance = (100,100)

    def getPoint(initPoint=(-1,-1)):

        if(initPoint==(-1,-1)):
            initPoint (shape_center[0]+random.randint(-shape_variance[0],shape_variance[0]),
                shape_center[1]+random.randint(-shape_variance[1],shape_variance[1]))


        angle = random.randint(0,360)
        segment_len = random.randint(segment_length[0],segment_length[1])
        x = initPoint[0]+segment_len * sin(angle)
        y = initPoint[1]+segment_len * cos(angle)


def newMain():

    global countrySylables
    global firstNames
    global properTitles

    #print item()
    #print adjectives[random.randint(5,len(adjectives)-6)]

    #clean the names
    newNames = []
    for i in range(0,len(firstNames)):
        newNames.append(firstNames[i].split())
    firstNames = sum(newNames,[])

    #clean the titles
    newNames = []
    for i in range(0,len(properTitles)):
        newNames.append(properTitles[i].split())
    properTitles = sum(newNames,[])

    #clean and sylabate the country names
    countrySylables = split_by_syllable(countryNames)

    for i in range(0,10):
        #print descriptive_area()
        print name()

newMain()
