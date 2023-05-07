from games.barca.players.minimax import MinimaxPlayer
from games.barca.simulator import BarcaSimulator
from games.barca.players.human_player import HumanPlayer
from games.game_simulator import GameSimulator

def run_simulation(desc: str, simulator: GameSimulator, iterations: int):
    print(f"----- {desc} -----")

    for i in range(0, iterations):
        simulator.change_player_positions()
        simulator.run_simulation()

    print("Results for the game:")
    simulator.print_stats()


def main():
    num_iterations = 1

    run_simulation("Maquina vs C.A.V.A.S", BarcaSimulator(HumanPlayer("C.A.V.A.S"), MinimaxPlayer("Take It Easy")), num_iterations)
    run_simulation("Maquina vs C.A.V.A.S", BarcaSimulator(MinimaxPlayer("Take It Down"), MinimaxPlayer("Take It Easy")), num_iterations)
    run_simulation("Maquina vs C.A.V.A.S", BarcaSimulator(HumanPlayer("C.A.V.A.S"), HumanPlayer("Take It Easy")), num_iterations)

if __name__ == "__main__":
    main()
