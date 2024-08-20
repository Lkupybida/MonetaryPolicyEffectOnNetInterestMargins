library(readr)
library(dplyr)
library(stargazer)
library(forecast)
library(lubridate)
library(stats)
library(lfe)

test_lag_combinations <- function(data, max_lag, output=FALSE) {
  best_model <- felm(NII ~ AE + LEV + CASH + NCI + SEC + TA + IR, data = data)
  best_aic <- AIC(best_model)
  print(best_aic)
  
  for (include_non_lagged in c(FALSE, TRUE)) {
    for (i in 1:max_lag) {
      for (combination in combn(1:max_lag, i, simplify = FALSE)) {
        if (include_non_lagged) {
          formula <- as.formula(paste("NII ~ AE + LEV + CASH + NCI + SEC + TA + IR +", paste(paste0("IR_lag", combination), collapse = " + ")))
        } else {
          formula <- as.formula(paste("NII ~ AE + LEV + CASH + NCI + SEC + TA + ", paste(paste0("IR_lag", combination), collapse = " + ")))
        }
        model <- felm(formula, data = data)
        current_aic <- AIC(model)
        if (output == TRUE) {
          cat("Best model formula: \n")
          cat(deparse(formula(model)))
          cat("\nAIC: ", current_aic, "\n\n") }
        if (current_aic < best_aic) {
          best_model <- model
          best_aic <- current_aic
        }
      }
    }
  }
  cat("Best model formula: \n")
  cat(deparse(formula(model)))
  return(best_model)
}


generate_stargazer_with_titles <- function(models, titles) {
  library(stargazer)
  
  type = "text"
  align = TRUE
  single_row = TRUE
  
  if (length(models) != length(titles)) {
    stop("The number of titles must match the number of models.")
  }
  
  # Calculate AIC scores
  aic_scores <- sapply(models, AIC)
  
  # Generate stargazer output
  output <- capture.output(
    stargazer(models, type = type, align = align, single.row = single_row)
  )
  
  # Remove quotes and leading numbers
  output <- gsub('^\\s*\\[\\d+\\]\\s*"|"$', '', output)
  
  # Find the position of the first separator line
  separator_line <- which(grepl("^=+$", output))[1]
  
  # Extract the width of the separator line
  total_width <- nchar(output[separator_line])
  
  # Calculate the width for each title
  title_width <- floor(total_width / length(titles))
  
  # Create aligned titles
  aligned_titles <- paste("", sapply(titles, function(t) sprintf(paste0("%-", title_width, "s"), t)), collapse = "")
  
  # Insert aligned titles at the top
  output <- c(aligned_titles, output)
  
  # Create AIC score row
  aic_row <- gsub("Adjusted R2", "AIC", output[grep("Adjusted R2", output)])
  aic_values <- sprintf("%.2f", aic_scores)
  aic_row <- gsub("\\d+\\.\\d+", "%s", aic_row)
  aic_row <- do.call(sprintf, c(list(aic_row), as.list(aic_values)))
  
  # Find the position to insert AIC scores (after Adjusted R2 line)
  adj_r2_line <- grep("Adjusted R2", output)
  
  # Insert AIC scores
  output <- c(output[1:adj_r2_line], aic_row, output[(adj_r2_line+1):length(output)])
  
  # Print the modified output
  cat(output, sep = "\n")
}