from knn_related import *
# Se importa el mean_digits de knn related

# 2. Mostrar las matrices de los promedios de cada dígito utilizando matplotlib

fig, axes = plt.subplots(2, 5, figsize=(10, 5))
x_ticks = np.arange(0, 8, 1)
y_ticks = np.arange(0, 8, 1)
for digit in range(10):
    ax = axes[digit//5, digit%5]
    ax.imshow(mean_digits[digit], cmap="gray_r")
    ax.set_xticks(x_ticks)
    ax.set_yticks(y_ticks)

    # for j in range(8):
    #     for i in range(8):
    #         ax.text(i, j, int(mean_digits[digit, j, i]), color="red" ,ha="center", va="center", fontsize=6)

    ax.set_title(str(digit))
# Se guarda la figura

plt.tight_layout()
plt.show()
fig.savefig("mean_digits.png")