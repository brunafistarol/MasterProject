# Dependencies -----------------------------------------------------------------

require(diffuStats)
require(igraph)
require("RcppCNPy")

# Loading the ppi ---------------------------------------------------------------

ppi <- read.csv('path\\MasterProject\\Salmonella\\ppi.csv')
ppi <- ppi[,-1]
ppi[,1] <- as.character(ppi[,1])
ppi[,2] <- as.character(ppi[,2])

# Creating PPI graph -----------------------------------------------------------

edges_list <- as.matrix(ppi[,1:2])

G <- graph.edgelist(edges_list, directed=F)

if (ncol(ppi) == 3)
  E(G)$weight <- ppi[,3]

vertices <- names(V(G))

# Computing kernel -------------------------------------------------------------

kernel <- "pStepKernel"

p <- 2

f <- match.fun(kernel)

{if (kernel == "pStepKernel") {
  K <- f(G, p=as.numeric(p))
  }
  else {
    K <- f(G)
  }}



# Convert to numpy -----------------------------------------------------------
names <- matrix(rownames(K), ncol=1)
write.csv(names, 'path\\MasterProject\\bacteria\\protein_names.txt', quote=FALSE, row.names=FALSE)
npySave(paste0("path\\MasterProject\\bacteria\\", kernel, "_", p, ".npy"), K, mode="w")
