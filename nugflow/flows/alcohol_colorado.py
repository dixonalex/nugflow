from metaflow import FlowSpec, step
import nugflow.domain.alcohol.colorado as co
from nugflow.config import bootstrap
from nugflow.domain.alcohol.colorado.transform import build_dfs


class AlcoholColoradoFlow(FlowSpec):
    """
    The next version of our playlist generator that adds a 'hint' parameter to
    choose a bonus movie closest to the 'hint'.

    The flow performs the following steps:

    1) Load the genre specific statistics from the MovieStatsFlow.
    2) In parallel branches:
       - A) Build a playlist from the top films in the requested genre.
       - B) Choose a bonus movie that has the closest string edit distance to
         the user supplied hint.
    3) Join the two to create a movie playlist and display it.

    """

    # genre = Parameter('genre',
    #                   help="Filter movies for a particular genre.",
    #                   default='Sci-Fi')
    #
    # hint = Parameter('hint',
    #                  help="Give a hint to the bonus movie algorithm.",
    #                  default='Metaflow Release')
    #
    # recommendations = Parameter('recommendations',
    #                             help="The number of movies recommended for "
    #                                  "the playlist.",
    #                             default=5)

    @step
    def start(self):
        """
        Use the Metaflow client to retrieve the latest successful run from our
        MovieStatsFlow and assign them as data artifacts in this flow.

        This step uses 'conda' to isolate the environment. This step will
        always use pandas==0.24.2 regardless of what is installed on the
        system.

        """
        from metaflow import get_metadata
        print("Using metadata provider: %s" % get_metadata())

        self.next(self.extract)

    @step
    def extract(self):
        """
        Use the user supplied 'hint' argument to choose a bonus movie that has
        the closest string edit distance to the hint.

        This step uses 'conda' to isolate the environment. Note that the
        package 'editdistance' need not be installed in your python
        environment.

        """
        timestamp = self.extract.created_at
        self._steps
        df = co.extract()
        self.liquor_license_data = df

        self.next(self.transform)

    @step
    def transform(self):
        """
        Select the top performing movies from the use specified genre.

        This step uses 'conda' to isolate the environment. This step will
        always use pandas==0.24.2 regardless of what is installed on the
        system.

        """
        df = self.liquor_license_data
        timestamp = self.transform.created_at

        tables = build_dfs(df, timestamp)
        self.tables = tables

        self.next(self.load)

    @step
    def load(self):
        """
        Join our parallel branches and merge results,

        """
        for table in self.tables:
            print(table)

        self.next(self.end)

    @step
    def end(self):
        """
        This step simply prints out the playlist.
        """
        print("le fin")


if __name__ == '__main__':
    bootstrap()
    AlcoholColoradoFlow()
