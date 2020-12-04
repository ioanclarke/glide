import engine
import arcade as arc

def main():
	#Create engine and window
	eng = engine.Engine()
	eng.create_window()
	eng.setup_menu(eng)

	#Run the game
	arc.run()
if __name__ == "__main__":
	main()