#!/usr/bin/python

'''
    @author Managarmr
    @version 1.0
    @code Pokemons' team generator (for sword and shield only)
    @date 23/12/2019
'''

# import
import argparse
import random
import copy

# définition des faiblesses de chaque type
weakness = [
            ['acier',['combat','feu','sol']],
            ['combat',['fee','psy','vol']],
            ['dragon',['dragon','fee','glace']],
            ['eau',['electrique','plante']],
            ['electrique',['sol']],
            ['fee',['acier','poison']],
            ['feu',['eau','roche','sol']],
            ['glace',['acier','combat','feu','roche']],
            ['insecte',['feu','roche','vol']],
            ['normal',['combat']],
            ['plante',['feu','glace','insecte','poison','vol']],
            ['poison',['psy','sol']],
            ['psy',['insecte','spectre','tenebres',]],
            ['roche',['acier','combat','eau','plante','sol']],
            ['sol',['eau','glace','plante']],
            ['spectre',['spectre','tenebres']],
            ['tenebres',['combat','fee','insecte']],
            ['vol',['electrique','glace','roche']]
           ]

# récupération des arguments
def argparser():
    '''
        parameters function
    '''
    parser = argparse.ArgumentParser(description='Pokemon list and conditions')
    parser.add_argument('list',help='a file containing the list of pokemon with struct: pokemon;gen;type;version')
    parser.add_argument('conditions',help='a file with conditions for generate team')
    parser.add_argument('--verbose',help='verbose mode',action='store_true')
    return parser.parse_args()

# récupération du fichier contenant la liste des pokemons
def arrayFromFile(file,verbose):
    '''
        get pokemons' data from file and put it into an array
        @file: pokemons'filename [string]
        @verbose: verbose mode [boolean]
    '''
    file = open(file,'r')
    pokemon,gen,types,version,evolved = [],[],[],[],[]
    for line in file:
        if (verbose):
            print(line)
        words = line.split('#')[0].split('\n')[0].split(';')
        if (verbose):
            print(words)
        pokemon.append(words[0])
        gen.append(int(words[1]))
        types.append(words[2])
        version.append(words[3])
        evolved.append(words[4])
    if (verbose):
        print(pokemon,gen,types,version,evolved)
    return pokemon,gen,types,version,evolved

# lecture des conditions
def readConditions(file,verbose):
    '''
        get conditions for team's generator
        @file: conditions'filename [string]
        @verbose: verbose mode [boolean]
    '''
    file = open(file,'r')
    array = []
    for line in file:
        if (verbose):
            print(line)
        if ('#' in line) or ('&' in line):
            continue
        condition = line.split('\n')[0].split('=')
        array.append(condition)
        if (verbose):
            print(condition)
    if (verbose):
        print(array)
    return array

# génération d'équipe avec des pokemons de types différents
def generateWithDifferentType(pokemonList,types,pokemon,pokemonType,verbose):
    '''
        generate pokemon team with different types
        @pokemonList: list of pokemons [array of string]
        @types: list of types [array of string]
        @pokemon: a pokemon must be in the team [string]
        @pokemonType: the type of pokemon [string]
        @verbose: verbose mode [boolean]
    '''
    team = []
    listType = []

    if not (pokemon == None):
        team.append(pokemon)
        pokemonType = pokemonType.split('/')
        for typ in pokemonType:
            listType.append(typ)

    while (len(team) < 6):
        index = random.randrange(len(pokemonList))
        if (pokemonList[index] not in team):
            typ = types[index].split('/')
            check =  [t for t in typ if (t in listType)]
            if (len(check) < 1):
                team.append(pokemonList[index])
                for t in typ:
                    listType.append(t)
            if (verbose):
                print(check)
                print(listType)
    return team

# génération de l'équipe optimale répondant aux différents critères
def generateOptimum(pokemonList,types,pokemonSelected,pokemonType,verbose):
    '''
        generate optimum pokemon team
        @pokemonList: list of pokemons [array of string]
        @types: list of types [array of string]
        @pokemonSelected: a pokemon must be in the team [string]
        @pokemonType: the type of pokemon [string]
        @verbose: verbose mode [boolean]
    '''
    team = []
    weaknessCopy = copy.deepcopy(weakness)

    if not (pokemonSelected == None):
        team.append(pokemonSelected)
        typ = pokemonType.split('/')
        for t in typ:
            index = 0
            for w in weaknessCopy:
                if (t in w[1]):
                    weaknessCopy = weaknessCopy[:index] + weaknessCopy[index+1:]
                else:
                    index += 1

    if (verbose):
        print(weaknessCopy)

    while (len(weaknessCopy) > 0) and (len(team) < 6):
        count = [
                    ('acier',0),
                    ('combat',0),
                    ('dragon',0),
                    ('eau',0),
                    ('electrique',0),
                    ('fee',0),
                    ('feu',0),
                    ('glace',0),
                    ('insecte',0),
                    ('normal',0),
                    ('plante',0),
                    ('poison',0),
                    ('psy',0),
                    ('roche',0),
                    ('sol',0),
                    ('spectre',0),
                    ('tenebres',0),
                    ('vol',0),
                ]
        # find the most interesting element
        bestElement = None
        for el,w in weaknessCopy:
            index = 0
            for elmt,c in count:
                if (bestElement == None):
                    bestElement = count[index]
                if (elmt in w):
                    count[index] = (elmt,c+1)
                    if (bestElement[1] < c+1): 
                        bestElement = count[index]
                index += 1
        if (verbose):
            print(count)
            print(bestElement)
            print(len(weaknessCopy))

        # find randomly a pokemon with a best type
        index = random.randrange(len(types))
        while (bestElement[0] not in types[index]):# or ('/' not in types[index]):
            index = random.randrange(len(types))

        # adding pokemon in the team
        if (pokemonList[index] not in team):
            team.append(pokemonList[index])
            typ = types[index].split('/')

            if (verbose):
                print(pokemonList[index])
                print(types[index])

            # remove element in weakness array
            for t in typ:
                index = 0
                for w in weaknessCopy:
                    if (t in w[1]):
                        weaknessCopy = weaknessCopy[:index] + weaknessCopy[index+1:]
                    else:
                        index += 1

        if (verbose):
            print(len(weaknessCopy))
            print(team)

    if (verbose):
        if (len(weaknessCopy) > 0):
            print("Remaining weakness : ",weaknessCopy)
        else:
            print("No remaining weakness !")

    return team

# generation des équipes
def generate(conditionsList,pokemonList,genList,types,version,evolved,verbose):
    '''
    '''
    count = 0
    maxTeam = 1
    teams = []
    versionRemoved = None
    pokemonType = None
    pokemonSelected = None

    if (verbose):
        print(conditionsList)

    optimum = conditionsList[0][1]
    only_type = conditionsList[1][1]
    same_type = conditionsList[2][1]
    pokemon = conditionsList[3][1]
    multi_team = conditionsList[4][1]
    ban = conditionsList[5][1]
    leg = conditionsList[6][1]
    gen = conditionsList[7][1]
    version = conditionsList[8][1]
    evo = conditionsList[9][1]

    # check if the parameters are compatible
    if (same_type == 'False') and not (only_type == 'False'):
        print("same_type and only_type are excluded parameters !")
        print("It's not possible to return a team !")
        return

    # if you need a specifid pokemon in your team
    if not (pokemon == 'False'):
        if (pokemon not in pokemonList):
            print(pokemon+" doesn't exist in pokemon list")
            print("You may not have written the name of the pokemon correctly. Only one pokemon name is expected.")
            return
        pokemonSelected = pokemon
        index = pokemonList.index(pokemon)
        pokemonList = pokemonList[:index] + pokemonList[index+1:]
        genList = genList[:index] + genList[index+1:]
        pokemonType = types[index]
        types = types[:index] + types[index+1:]
        version = version[:index] + version[index+1:]
        evolved = evolved[:index] + evolved[index+1:]

    # each pokemon of the team must have a predefine type (and a second type with this predefine type)
    if not (only_type == 'False'):
        for typ in types:
            if not (only_type in typ):
                index = types.index(typ)
                types = types[:index] + types[index+1:]
                evolved = evolved[:index] + evolved[index+1:]
                version = version[:index] + version[index+1:]
                pokemonList = pokemonList[:index] + pokemonList[index+1:]
                genList = genList[:index] + genList[index+1:]

    # return many teams
    if (multi_team == 'True'):
        maxTeam = 10

    # remove banned pokemons
    if not (ban == 'False'):
        pokemonBanned = ban.split(';')
        for pkm in pokemonBanned:
            if (pkm in pokemonList):
                index = pokemonList.index(pkm)
                pokemonList.remove(pkm)
                genList = genList[:index] + genList[index+1:]
                types = types[:index] + types[index+1:]
                version = version[:index] + version[index+1:]
                evolved = evolved[:index] + evolved[index+1:]

    # remove legendaries pokemon
    if (leg == 'False'):
        pokemonBanned = ['Zacian','Zamazenta','Ethernatos']
        for pkm in pokemonBanned:
            if (pkm in pokemonList):
                index = pokemonList.index(pkm)
                pokemonList.remove(pkm)
                genList = genList[:index] + genList[index+1:]
                types = types[:index] + types[index+1:]
                version = version[:index] + version[index+1:]
                evolved = evolved[:index] + evolved[index+1:]

    # select specific gen
    if not (gen == 'False'):
        gen = gen.split(';')
        genAuthorized = []
        for element in gen:
            element = int(element)
            if (element < 1 or element > 8):
                print("This generation doesn't exist")
                return
            genAuthorized.append(element)

        for generation in genList:
            if not (generation in genAuthorized):
                index = genList.index(generation)
                genList = genList[:index] + genList[index+1:]
                pokemonList = pokemonList[:index] + pokemonList[index+1:]
                types = types[:index] + types[index+1:]
                version = version[:index] + version[index+1:]
                evolved = evolved[:index] + evolved[index+1:]
    
    # select a specific version
    if (version == 'bouclier') or (version == 'shield'):
        versionRemoved = 'epee'
    elif (version == 'epee') or (version == 'sword'):
        versionRemoved = 'bouclier'
    for v in version:
        if (v == versionRemoved):
            index = version.index(v)
            version = version[:index] + version[index+1:]
            pokemonList = pokemonList[:index] + pokemonList[index+1:]
            genList = genList[:index] + genList[index+1:]
            types = types[:index] + types[index+1:]
            evolved = evolved[:index] + evolved[index+1:]

    # evolved only
    if (evo == 'True'):
        for evolve in evolved:
            if not (evolve == '+'):
                index = evolved.index(evolve)
                evolved = evolved[:index] + evolved[index+1:]
                version = version[:index] + version[index+1:]
                pokemonList = pokemonList[:index] + pokemonList[index+1:]
                genList = genList[:index] + genList[index+1:]
                types = types[:index] + types[index+1:]

    # if the pokemon list is too short
    if (len(pokemonList) < 6):
        print("It's not possible to return a team of 6 pokemons with these conditions")
        print(pokemonList)
        return

    if (verbose):
        print(pokemonList)

    while (count < maxTeam):
        # find the optimum team
        if (optimum == 'True'):
            team = generateOptimum(pokemonList,types,pokemonSelected,pokemonType,verbose)
        # don't allow pokemon with the same type in a team
        elif (same_type == 'False'):
            team = generateWithDifferentType(pokemonList,types,pokemonSelected,pokemonType,verbose)
        else:
            # add the specific pokemon
            if not (pokemon == 'False'):
                team = random.sample(pokemonList,5)
                team.append(pokemon)
            else:
                team = random.sample(pokemonList,6)

        teams.append(team)
        count += 1

    # display the team
    for team in teams:
        if (len(team) < 6):
            print("Optimal element team found without reaching the 6 pokemons.")
            print("You can therefore complete the following team as you wish.")
        print(team)

# main
def main():
    arg = argparser()
    pokemonFile = arg.list
    conditions = arg.conditions
    verbose = arg.verbose

    pokemon,gen,types,version,evolved = arrayFromFile(pokemonFile,verbose)
    conditionsList = readConditions(conditions,verbose)
    generate(conditionsList,pokemon,gen,types,version,evolved,verbose)

if __name__ == "__main__":
    main()