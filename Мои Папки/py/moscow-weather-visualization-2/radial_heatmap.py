import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from typing import Tuple, List, Generator, T, Union
from bisect import bisect_left
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle
def dataframes() -> Generator[pd.DataFrame, None, None]:
    # read dataframe from file path and split into 6
    df = pd.read_excel(r"C:\Users\Gleb\Мои Папки\py\school_project\weather_data_final.xlsx", index_col = 0)
    dfs = np.array_split(df, 6)
    for i in dfs:
        yield i
def colors_thresholds() -> Tuple[list]:
    values = [-40, -30, -20, -15, -10, -5, 0, 5, 10, 15, 20, 25, 30, 40, 50]
    colors = ['#eeeeee', '#ffaaff', '#910991', '#24186a', '#554eb1',
              '#3e79c6', '#4bb698', '#59d049', '#bee43d', '#ebd735',
              '#eaa43e', '#e56d53', '#be3066', '#6b1528', '#2b0001']
    return values, colors
def df_colors(df: pd.DataFrame) -> List[str]:
    # turn dataframe values to list of hex colors
    values = df.values.flatten()
    thresh_values, thresh_colors = colors_thresholds()
    colors = []
    for val in values:
        colors.append(thresh_colors[bisect_left(thresh_values, val)-1])
    return colors
def list_split(lst: List[T], n: int) -> List[T]:
    return [lst[i:i + n] for i in range(0, len(lst), n)]
def bar_length(min_val: float, max_val: float, val: float) -> float:
    return abs(min_val - val) / abs(min_val - max_val)
class Plotter:
    def __init__(self,
                 axes: plt.Axes,
                 df: pd.DataFrame,
                 total_radius: float,
                 empty_radius: float,
                 bar_min: float,
                 bar_max: float,
                 empty_color: Union[str, tuple, float],
                 circle_labels: List[T],
                 circle_labels_size: float,
                 thresh_show: bool,
                 thresh_amount: int,
                 thresh_labels: List[T],
                 thresh_labels_size: float,
                 thresh_style: str,
                 thresh_color: Union[str, tuple, float],
                 thresh_alpha: float,
                 legend_show: bool,
                 legend_cords: Tuple[float],
                 title_primary: str,
                 title_secondary: str,
                 title_primary_height: float,
                 title_secondary_height: float,
                 title_size: float) -> None:
        # pass user-provided variables
        self.axes = axes
        self.df = df
        self.total_radius = total_radius
        self.empty_radius = empty_radius
        self.bar_min = bar_min
        self.bar_max = bar_max
        self.empty_color = empty_color
        self.circle_labels = circle_labels
        self.circle_labels_size = circle_labels_size
        self.thresh_show = thresh_show
        self.thresh_amount = thresh_amount
        self.thresh_labels = thresh_labels
        self.thresh_labels_size = thresh_labels_size
        self.thresh_style = thresh_style
        self.thresh_color = thresh_color
        self.thresh_alpha = thresh_alpha
        self.legend_show = legend_show
        self.legend_cords = legend_cords
        self.title_primary = title_primary
        self.title_secondary = title_secondary
        self.title_primary_height = title_primary_height
        self.title_secondary_height = title_secondary_height
        self.title_size = title_size
        # pass technical variables
        self.x_size = df.shape[1]
        self.y_size = df.shape[0]
        radii = np.linspace(self.total_radius/self.y_size,
                            self.total_radius, self.y_size)
        self.radii = (radii+self.empty_radius)[::-1]
        df["mean"] = df.mean(axis=1)
        colors = df_colors(df)
        colors = list_split(colors, self.x_size + 1)
        self.heatmap_colors = [i[:-1] for i in colors]
        self.bar_chart_colors = [[i[-1]] + [self.empty_color] for i in colors]
        self.heatmap_sizes = [1 / self.x_size] * self.x_size
        self.bar_chart_sizes = [bar_length(self.bar_min, self.bar_max, i)
                               for i in df[df.columns[-1]]]

        self.bar_chart_empty = [abs(1-i) for i in self.bar_chart_sizes]
        self.wedgeprops = {"edgecolor" : "black",
                           'linewidth': 0.5,
                           'antialiased': True}
    def radial_heatmap(self) -> None:
        # plot concentric pie charts
        for i, (radius, color_list) in enumerate(zip(self.radii,
                                                 self.heatmap_colors)):
            try:
                labels = self.circle_labels[::-1] if i == 0 else None
            except TypeError:
                labels = None
            (self.axes[0]).pie(self.heatmap_sizes,
                               radius = radius,
                               colors = color_list[::-1],
                               startangle = 90,
                               labels = labels,
                               labeldistance = 1.075,
                               textprops={'fontsize': self.circle_labels_size},
                               wedgeprops = self.wedgeprops,
                               normalize = True)
        # add empty pie chart in the center to make a donut
        (self.axes[0]).pie([100], radius = self.empty_radius,
                           colors = [self.empty_color],
                           wedgeprops = self.wedgeprops)
        (self.axes[0]).axis("equal")
    def bar_chart(self) -> None:
        # plot concentric radial bar charts
        for (radius, color_list,
             bar_size, empty_size) in zip(self.radii,
                                          self.bar_chart_colors,
                                          self.bar_chart_sizes,
                                          self.bar_chart_empty):
            (self.axes[1]).pie([empty_size, bar_size],
                               radius = radius,
                               colors = color_list[::-1],
                               startangle = 90,
                               normalize = True,
                               wedgeprops = self.wedgeprops)
        (self.axes[1]).pie([100], radius = self.empty_radius,
                        colors = [self.empty_color],
                           wedgeprops = self.wedgeprops)
        (self.axes[1]).axis("equal")        
    def thresh_lines(self) -> None:
        # add threshold lines to radial bar charts
        if self.thresh_show:
            vals = np.deg2rad(np.linspace(0, 360, self.thresh_amount, False))
            full_radius = self.total_radius + self.empty_radius
            for x, y, label in zip(np.sin(vals), np.cos(vals), self.thresh_labels):
                (self.axes[1]).plot([x * full_radius, x * self.empty_radius],
                                    [y * full_radius, y * self.empty_radius],
                                    c = self.thresh_color, ls = self.thresh_style,
                                    linewidth = 2, alpha = self.thresh_alpha)
                (self.axes[1]).text(x * full_radius * 1.2, y * full_radius * 1.2,
                                    label, ha = "center", va = "center",
                                    fontsize = self.thresh_labels_size)
    def legend(self) -> None:
        # create color legend from colors_thresholds()
        if self.legend_show:
            thresh_values, thresh_colors = colors_thresholds()
            lines = [Line2D([0], [0], color = color, lw = 5) for color in thresh_colors]
            (self.axes[0]).legend(lines, [f"{i}°C" for i in thresh_values],
                                  bbox_to_anchor = self.legend_cords,
                                  prop={'size': 22})
    def title(self) -> None:
        # add titles to axis
        for ax, title, height in zip(self.axes, [self.title_primary, self.title_secondary],
                             [self.title_primary_height, self.title_secondary_height]):
            ax.text(0, (self.total_radius + self.empty_radius) * height,
                    title, ha = "center", va = "center",
                    fontsize = self.title_size)
def main() -> None:
    plt.style.use("seaborn")
    fig, (axes) = plt.subplots(2, 6, figsize = (55, 25))
    axes = axes.flatten()
    # create labels for months and thresholds
    circle_labels = ['янв.', 'фев.', 'мар.', 'апр.', 'май.', 'июн.',
                     'июл.', 'авг.', 'сен.', 'окт.', 'ноя.', 'дек.']
    thresh_labels = [f"{round(i, 3)}°C" for i in np.linspace(0, 10, 9)]
    thresh_labels = [f"{thresh_labels[0]} | {thresh_labels[-1]}"] + thresh_labels[1:-1]
    for ax0, ax1, df, legend_show in zip(axes[0:6], axes[6:12], dataframes(),
                                         [True] + [False] * 5):
        index = df.index.tolist()
        plot = Plotter(axes = (ax0, ax1),
                       df = df,
                       total_radius = 12,
                       empty_radius = 7,
                       bar_min = 0,
                       bar_max = 10,
                       empty_color = "white",
                       circle_labels = circle_labels,
                       circle_labels_size = 20,
                       thresh_show = True,
                       thresh_amount = 8,
                       thresh_labels = thresh_labels,
                       thresh_labels_size = 20,
                       thresh_style = "-",
                       thresh_color = "black",
                       thresh_alpha = 0.3,
                       legend_show = legend_show,
                       legend_cords = (-0.125, 1),
                       title_primary = (
                           f"среднемесячная температура\nс "
                           f"{index[0]} по {index[-1]}"
                           ),
                       title_secondary = (
                           f"среднегодовая температура\nс "
                           f"{index[0]} по {index[-1]}"
                           ),
                       title_primary_height = 1.3,
                       title_secondary_height = 1.5,
                       title_size = 24)
        plot.radial_heatmap()
        plot.bar_chart()
        plot.thresh_lines()
        plot.legend()
        plot.title()
    # add main title
    fig.suptitle(("Температура воздуха в Москве с 1871 по 2020\n"
                 "Один круг равен одному году (по возрастанию:\n"
                  "самый широкий круг равен первому указанному году)\n"
                  "Температуры помечены цветами"),
                 fontsize = 27, y = 0.94)
    plt.savefig("weather_data_moscow.png")
if __name__ == "__main__":
    main()

               
               
            
                                    
            
            
        
                            
        
                            
                            
        
        
    
    
    
                 
