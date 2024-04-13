ifeq ($(OS),Windows_NT)
	DELETE_FILE = del /Q
	DELETE_FOLDER = rmdir /S /Q
else
	DELETE_FILE = rm -rf
	DELETE_FOLDER = rm -rf
endif

SRC = src/fr/asqel/ultravel

SRCS = $(wildcard $(SRC)/*.java) $(wildcard $(SRC)/*/*.java) $(wildcard $(SRC)/*/*/*.java)

BINS = tmp

OUT = game.jar

all:
	javac $(SRCS) -d $(BINS)
	jar cfm $(OUT) META-INF/MANIFEST.MF -C $(BINS) .  -C src assets


run:
	java -jar game.jar
clean:
	$(DELETE_FILE) $(OUT)
	$(DELETE_FOLDER) $(BINS)
