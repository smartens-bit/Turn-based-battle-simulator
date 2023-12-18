import random

class Creature:
    def __init__(self, name, max_hp=10):
        self.name = name
        self.hp = max_hp
        self.max_hp = max_hp
        self.abilities = {'Attack': 1, 'Defence': 5, 'Speed': 5}

    def check_life(self):
        if self.hp <= 0:
            self.hp = 0
            print(f"{self.name} fainted...")
            return False
        return True

    def attack(self, target):
        roll = random.randint(1, 20)
        if roll < target.abilities['Defence'] + target.abilities['Speed']:
            print(f"{self.name} attacks {target.name}")
            print(f"{self.name}'s attack missed...")
        else:
            damage = self.abilities['Attack'] + random.randint(1, 4)
            target.hp -= damage
            print(f"{self.name} attacks {target.name}")
            print(f"Attack hits for {damage} damage!")
            return target.check_life()

    def turn(self, target_list):
        return self.attack(target_list)
    
    def auto_select(self, target_list):
        target_list = [creature for creature in target_list if not creature.check_life()]
        if target_list:
            return random.choice(target_list)
        else:
            return None

class Goblin(Creature):
    def __init__(self, name):
        super().__init__(name, max_hp=15) 

class Orc(Creature):
    def __init__(self, name, max_hp=50):
        super().__init__(name)
        self.max_hp = max_hp
        self.hp = self.max_hp
        self.abilities = {'Attack': 5, 'Defence': 8, 'Speed': 3}
        self.abilities_mod = False
        self.turn_counter = 0

    def heavy_attack(self, target):
        if not self.abilities_mod:
            self.abilities['Attack'] += 5
            self.abilities['Defence'] -= 3
            self.abilities_mod = True
            print(f"{self.name} is in rage! His Attacking stats have increased by 5 hit points, but his defence has lowered by 3.")
        return super().attack(target)

    def attack(self, target):
        if self.abilities_mod:
            self.abilities_mod = False
            print(f"{self.name} has cooled down. His attacking and defensive stats have been restored.")
        return super().attack(target)

    def turn(self, target):
        self.turn_counter += 1
        if self.turn_counter % 4 == 0:
            result = self.heavy_attack(target)
            self.abilities['Attack'] -= 5
            self.abilities['Defence'] += 3
            self.abilities_mod = True
            return result
        else:
            return self.attack(target)
        
class Warrior(Creature):
    def __init__(self, name):
        super().__init__(name)
        self.hp = 50
        self.abilities = {'Attack': 5, 'Defence': 10, 'Speed': 4}
        self.shield_up_attack = False
        self.turn_counter = 0

    def shield_up(self):
        if not self.shield_up_attack:
            self.abilities['Attack'] -= 4
            self.abilities['Defence'] += 4
            self.shield_up_attack = True
            print(f"{self.name} raises the shield! Attack reduced by 4 and Defence increased by 4.")

    def shield_down(self):
        if self.shield_up_attack:
            self.abilities['Attack'] = 5
            self.abilities['Defence'] = 10
            self.shield_up_attack = False
            print(f"{self.name} lowers the shield! Attack and Defence restored to original values.")

    def turn(self, target):
        self.turn_counter += 1
        if self.turn_counter % 4 == 1:
            self.attack(target)
            self.shield_up()
        elif self.turn_counter % 4 == 0:
            self.shield_down()
            self.attack(target)
        else:
            self.attack(target)
            
class Archer(Creature):
    def __init__(self, name, max_hp=30):
        super().__init__(name, max_hp=max_hp)
        self.abilities = {'Attack': 7, 'Defence': 9, 'Speed': 8}
        self.abilities_mod = False
        self.turn_counter = 0 

    def power_shot(self, target):
        roll1 = random.randint(1, 20)
        roll2 = random.randint(1, 20)
        roll = max(roll1, roll2)

        if self.abilities['Speed'] > target.abilities['Speed']:
            roll += self.abilities['Speed'] - target.abilities['Speed']

        if not self.abilities_mod:
            self.abilities['Attack'] += 3
            self.abilities['Defence'] -= 3
            self.abilities_mod = True
            print(f"{self.name} uses power shot! His Attacking stats have increased by 3 hit points, but his defence has lowered by 3.")

        if roll >= target.abilities['Defence'] + target.abilities['Speed']:
            damage = self.abilities['Attack'] + random.randint(1, 8)
            target.hp -= damage
            print(f"{self.name} power shots {target.name} for {damage} damage!")
        else:
            print(f"{self.name}'s power shot missed")
        return target.check_life()

    def attack(self, target):
        if self.abilities_mod:
            self.abilities_mod = False
            print(f"{self.name} resets. His Attacking and Defensive stats have been restored.")
        return super().attack(target)
    
    def auto_select(self, target_list):
        selected_target = None
        min_hp = None 
        for creature in target_list:
            if not creature.check_life():
                if min_hp is None or creature.hp < min_hp:
                    min_hp = creature.hp
                    selected_target = creature
        return selected_target

    def turn(self, target):
        self.turn_counter += 1
        if self.turn_counter % 4 == 1:
            return self.attack(target)
        else:
            return self.power_shot(target)

class Fighter(Creature):
    def __init__(self, name):
        super().__init__(name, max_hp=50)
        self.abilities = {'Attack': 5, 'Defence': 8, 'Speed': 5}
    
    def turn(self, target):
        print(f"{self.name} unleashes a flurry of strikes.")
        if target.hp <= 0:
            return True
        for i in range(3):
            if i > 0:
                self.abilities['Attack'] -= 3
            self.attack(target)
        if target.hp >= 0:
            self.abilities['Attack'] = 5
        return target.hp >= 0
    
    def auto_select(self, target_list):
        selected_target = None
        max_hp = None  
        for creature in target_list:
            if not creature.check_life():
                if max_hp is None or creature.hp > max_hp:
                    max_hp = creature.hp
                    selected_target = creature
        return selected_target
    
class OrcGeneral(Orc, Warrior):
    def __init__(self, name):
        super().__init__(name) 
        Warrior.__init__(self, name)  
        self.turn_counter = 0
        self.hp = 80

    def turn(self, target):
        self.turn_counter += 1
        
        if self.turn_counter % 4 == 1:
            Orc.attack(self, target)  
            Warrior.shield_up(self)   
        elif self.turn_counter % 4 == 2:
            Orc.attack(self, target)
        elif self.turn_counter % 4 == 3:
            Warrior.shield_down(self) 
            Orc.attack(self, target)
        elif self.turn_counter % 4 == 0:
            Orc.heavy_attack(self, target)
            
class GoblinKing(Goblin, Archer):
    def __init__(self, name):
        Goblin.__init__(self, name)  
        Archer.__init__(self, name) 
        self.hp = 50

    def turn(self, target_list):
        Archer.turn(self, target_list)            

class Boss(Orc):
    def __init__(self, name):
        Orc.__init__(self, name)
        self.max_hp = 200
        self.hp = self.max_hp
        self.abilities = {'Attack': 5, 'Defence': 8, 'Speed': 5}

    def auto_select(self, target_list, mode):
        if mode == 'Strong':
            selected_target = max(target_list, key=lambda creature: creature.hp)
        elif mode == 'Weak':
            selected_target = min(target_list, key=lambda creature: creature.hp)
        elif mode == 'Random':
            selected_target = random.choice(target_list)
        else:
            selected_target = None
        return selected_target
    
    def turn(self, target):
        print(f"{self.name} unleashes a flurry of strikes.")
        if target.hp <= 0:
            return True
        for i in range(3):
            if i > 0:
                self.abilities['Attack'] -= 3
            self.attack(target)
        if target.hp >= 0:
            self.abilities['Attack'] = 5
        return target.hp >= 0

    def heavy_attack(self, target):
        if not self.abilities_mod:
            self.abilities['Attack'] += 5
            self.abilities['Defence'] -= 3
            self.abilities_mod = True
            print(f"{self.name} is in rage! His Attacking stats have increased by 5 hit points, but his defence has lowered by 3.")
        return super().attack(target)
        
    def turn(self, round_num, target_list):
        if round_num % 4 == 1:
            target = self.auto_select(target_list, 'Weak')
            if target:
                self.attack(target)
                if target.hp <= 0:
                    for _ in range(2):
                        target = self.auto_select(target_list, "Random")
                        if target:
                            self.attack(target)
                        else:
                            break
        else:
            target = self.auto_select(target_list, "Strong") 
            if target:
                self.heavy_attack(target)
                
class Wizard(Creature):
    def __init__(self, name, max_hp=20):
        super().__init__(name, max_hp)
        self.mana = 100
        self.abilities = {
            'Attack': 3,
            'Defence': 5,
            'Speed': 5,
            'Arcana': 10
        }
        
    def modify_mana(self, amount):
        self.mana = max(0, min(self.mana + amount, 100))

    def attack(self, target):
        super().attack(target)
        self.modify_mana(20)
        print("mana +20")
        
    def recharge(self):
        if self.mana >= 100:
            print(f"Mana is already full: {self.mana}")
            return
        else: 
            self.mana = min(self.mana + 30, 100)
            print("Mana +30")

    def fire_bolt(self, target):
        self.attack(target)
        damage = random.randrange(1, self.abilities['Arcana'] // 2)
        if damage > 0:
            target.hp -= damage
            print(f"{target.name} takes {damage} damage from Fire Bolt.")
        else:
            print(f"Attack missed!")
        self.mana += 10

    def heal(self, target):
        if self.mana < 20:
            print(f"Not enough Mana. Current Mana: {self.mana}")
            return
        amount_healed = random.randint(0, 8) + (self.abilities['Arcana'] // 2)
        if amount_healed > 0:
            target.hp = min(target.hp + amount_healed, target.max_hp)
            print(f"{self.name} heals {target.name} for {amount_healed} HP")
        else:
            print(f"Failed to heal!")
        self.mana -= 20

    def mass_heal(self, allies):
        if self.mana < 30:
            print(f"Not enough Mana. Current Mana: {self.mana}")
            return
        amount_healed = random.randint(0, 10) + self.abilities['Arcana']
        if amount_healed > 0:
            for ally in allies:
                ally.hp = min(ally.hp + amount_healed // 2, ally.max_hp)
                print(f"{self.name} heals {ally.name} for {amount_healed // 2} HP")
        else:
            print(f"Failed to heal!")
        self.mana -= 30

    def fire_storm(self, enemies):
        if self.mana < 50:
            print(f"Not enough Mana. Current Mana: {self.mana}")
            return
        half_arcana = self.abilities['Arcana'] // 2
        for enemy in enemies:
            random_number = random.randint(1, 20) + enemy.speed
            if random_number >= half_arcana:
                damaged = random.randint(5, 20) + half_arcana
                enemy.hp -= damaged // 2
                print(f"{enemy.name} takes {damaged // 2} damage from Fire Storm.")
            else:
                damaged = random.randint(5, 20) + half_arcana
                enemy.hp -= damaged
                print(f"{enemy.name} takes {damaged} damage from Fire Storm.")
        self.mana -= 50

    def select_target(self, target_list):
        for index, target in enumerate(target_list):
            print(f"{index + 1}. {target.name} - HP: {target.hp}/{target.max_hp}")

        while True:
            try:
                target_index = int(input("Choose target (Enter the index): "))
                if 1 <= target_index <= len(target_list):
                    return target_list[target_index - 1]
                print("Invalid index. Please enter a valid index.")
            except ValueError:
                print("Invalid input. Please enter an integer.")
                
    def turn(self, creature):
        print("\nIt's your turn! Choose an action:")
        print("1: Attack")
        print("2: Fire Bolt")
        print("3: Heal")
        print("4: Mass Heal")
        print("5: Fire Storm")

        action = input("Enter your action: ")

        if action in ['1', '2', '3']:
            target = self.select_target(creature)

            if target:  
                if action == '1':
                    self.attack(target)
                elif action == '2':
                    self.fire_bolt(target)
                elif action == '3':
                    self.heal(target)
        elif action == '4':
            self.mass_heal(creature)  
        elif action == '5':
            self.fire_storm(creature)  
        else:
            print("Please choose a valid number.")

           
def battle_sim():
    wizard = Wizard("Gandalf")
    archer = Archer("Legolas")
    fighter = Fighter("Aragorn")
    orc = Orc("Orc")

    targets = [fighter, archer, orc]

    for round_num in range(1, 21):
        print("\n--- Round", round_num, "---")

        wizard.turn(targets)
        
        for target in targets:
            if not target.check_life():
                print(f"{target.name} has been defeated!")
battle_sim()