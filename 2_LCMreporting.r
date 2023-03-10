library(ggplot2)
library(viridis)

data <-  data.frame(layername=character(0),x=double(0),dob=double(0))
x_values <- seq(0, 2000, by = .2) # Define the range of values for x

# Define the function
my_function <- function(x, a, b, c, w) {
  (1 / (1 + exp(((x / c) - a) * b))) * w
}

wgt_table <- read.csv(here::here("_data","input", "LCM_weights.csv"), stringsAsFactors=FALSE)

for(z in 1:nrow(wgt_table)){
  # Set the parameter values
  a <- wgt_table$a[z]
  b <- wgt_table$b[z]
  c <- wgt_table$c[z]
  w <- wgt_table$w[z]

  # Calculate the values of the function for each value of x
  y_values <- my_function(x_values, a, b, c, w)  
  
  # Combine the data into a data frame
  lyname <- unique(wgt_table[z,2])
  data1 <- data.frame(layername=lyname, x=x_values, y=y_values)
  data <- rbind(data, data1)
}


# Create the plot using ggplot2
ggplot(data, aes(x=x, y=y, group=layername, color=layername)) +
  geom_line(size=1.5) +
  #labs(title="Function Plot", x="x", y="y")
  scale_color_discrete() +
  ggtitle("Function Plot") +
  xlab("Distance (meters)") + ylab("Weight") +
  theme_classic() +
  theme(legend.position = c(.8, .8))
