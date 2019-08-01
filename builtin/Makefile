CC = g++

RM = rm

DEPS = generator.h
OBJ = ls12.o generator.o parser.o delay_bound.o rta_ss.o

PROJ = RTSS_FRED

CFLAGS = -std=c++11 -Wall -m64 -O3 -fPIC -fexceptions -DNDEBUG -DIL_STD -DILOSTRICTPOD -DILOUSEMT -D_REENTRANT -DILM_REENTRANT -g

ifdef runs
	CFLAGS += -DRUNS=$(runs)
else
	CFLAGS += -DRUNS=1
endif

INCLUDES = -I. -I/opt/ibm/ILOG/CPLEX_Studio_Community129/cpoptimizer/include -L/opt/ibm/ILOG/CPLEX_Studio_Community129/cpoptimizer/lib/x86-64_linux/static_pic -I/opt/ibm/ILOG/CPLEX_Studio_Community129/cplex/include -I/opt/ibm/ILOG/CPLEX_Studio_Community129/concert/include -L/opt/ibm/ILOG/CPLEX_Studio_Community129/cplex/lib/x86-64_linux/static_pic -L/opt/ibm/ILOG/CPLEX_Studio_Community129/concert/lib/x86-64_linux/static_pic
#INCLUDES = -I. -I/opt/ibm/ILOG/CPLEX_Studio128/cpoptimizer/include -L/opt/ibm/ILOG/CPLEX_Studio128/cpoptimizer/lib/x86-64_linux/static_pic -I/opt/ibm/ILOG/CPLEX_Studio128/cplex/include -I/opt/ibm/ILOG/CPLEX_Studio128/concert/include -L/opt/ibm/ILOG/CPLEX_Studio128/cplex/lib/x86-64_linux/static_pic -L/opt/ibm/ILOG/CPLEX_Studio128/concert/lib/x86-64_linux/static_pic

# LIBS = -Wl,--start-group -lconcert -lilocplex -lcp -lcplex -lemon -Wl,--end-group -ldl -lpthread -lm
LIBS = -Wl,--start-group -lconcert -lilocplex -lcp -lcplex -lemon -Wl,--end-group -ldl -lpthread -lm

ifeq ($(solver),GLPK)
	INCLUDES = -I.
	LIBS = -Wl,--start-group -lglpk -lemon -Wl,--end-group -lpthread -lm
else	
	CFLAGS += -D__RTA_SS_USE_CLEX__
endif

%.o: %.cpp $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

$(PROJ): $(OBJ)
	$(CC) -o $@ $^ $(CFLAGS) $(INCLUDES) $(LIBS)

clean:
	$(RM) -rf *.o $(PROJ)

