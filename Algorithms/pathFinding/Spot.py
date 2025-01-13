from Algorithms.pathFinding.SpotState import SpotState


class Spot:
    """
    A class to represent each Spot in A*

    ...

    Attributes
    ----------
    row : int
        Row position of Spot
    col : int
        Column position of Spot
    spot_state : SpotState
        Type of Spot
    neighbors: list[SpotState]
        The Spot that are adjacent to the current Spot
    total_rows: int
        The number of rows in the grid
    total_cols: int
        The number of columns in the grid
    """

    def __init__(
            self, row, col, total_rows, total_cols, spot_state: SpotState
    ) -> None:

        # The position in rows and columns
        self.row = row
        self.col = col

        # This determines if this spot can be moved through or not
        self.spot_state = spot_state

        # Each spot need to know which spot it is connected to and how close they are to the target
        self.neighbors = []

        # Used for check boundaries
        self.total_rows = total_rows
        self.total_cols = total_cols

    def get_pos(self) -> tuple:
        """
        Returns the position of the Spot

        Returns
        -------
        tuple
        """
        return self.col, self.row

    def is_closed(self) -> bool:
        """
        Returns the Spot is closed

        Returns
        -------
        bool
        """
        return self.spot_state == SpotState.CLOSE

    def is_open(self) -> bool:
        """
        Returns if the Spot is open

        Returns
        -------
        bool
        """
        return self.spot_state == SpotState.OPEN

    def is_barrier(self) -> bool:
        """
        Returns if the Spot is a barrier

        Returns
        -------
        bool
        """
        return self.spot_state == SpotState.BARRIER

    def is_start(self) -> bool:
        """
        Returns if the Spot is a start

        Returns
        -------
        bool
        """
        return self.spot_state == SpotState.START

    def is_end(self) -> bool:
        """
        Returns the Spot is an end

        Returns
        -------
        bool
        """
        return self.spot_state == SpotState.END

    def make_open(self) -> None:
        """
        Turns the Spot into Open

        Returns
        -------
        None
        """
        self.spot_state = SpotState.OPEN

    def make_end(self) -> None:
        """
        Turns the Spot into End

        Returns
        -------
        None
        """
        self.spot_state = SpotState.END

    def make_start(self) -> None:
        """
        Turns the Spot into Start

        Returns
        -------
        None
        """
        self.spot_state = SpotState.START

    def make_closed(self) -> None:
        """
        Turns the Spot into Close

        Returns
        -------
        None
        """
        self.spot_state = SpotState.CLOSE

    def update_neighbors(self, grid) -> None:
        """
        Updates all the current Spot's neighbor's states

        Parameters
        ----------
        grid : list[list[Spot]]
            The grid that the Spot is currently in

        Returns
        -------
        None
        """
        self.neighbors = []
        if (
                self.row < self.total_rows - 1
                and not grid[self.row + 1][self.col].is_barrier()
        ):  # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if (
                self.col < self.total_cols - 1
                and not grid[self.row][self.col + 1].is_barrier()
        ):  # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other) -> bool:
        """
        This makes sure that the less than operation always returns False

        Parameters
        ----------
        other : Spot
            The other Spot that is compared

        Returns
        -------
        bool
        """
        return False
