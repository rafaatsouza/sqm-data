class VisualizationMethods:
    
    @staticmethod
    def set_boxplots_by_ax(ax, data_dict, title, use_log_as_yscale_out=False):
        columns = sorted(data_dict.keys(), key=lambda x: x)

        for position, column in enumerate(columns):
            ax.boxplot(data_dict[column], positions=[position], flierprops=dict(markerfacecolor='g', marker='D'))

        ax.set_xticks(range(position+1))
        ax.set_xticklabels(columns)
        ax.set_xlim(xmin=-0.5)
        if use_log_as_yscale_out:
            ax.set_yscale('log')
        ax.set_title(title)
        ax.grid()
