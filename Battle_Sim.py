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
        target = self.auto_select(target_list)
        if target:
            self.attack(target)

    def auto_select(self, target_list):
        valid_targets = [creature for creature in target_list if creature.hp > 0]
        return random.choice(valid_targets) if valid_targets else None

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

    def turn(self, target_list):
        self.turn_counter += 1
        target = self.auto_select(target_list)
        if target is None:
            return

        if self.turn_counter % 4 == 0:
            self.heavy_attack(target)
            self.abilities['Attack'] -= 5
            self.abilities['Defence'] += 3
        else:
            self.attack(target)
        
class Warrior(Creature):
    def __init__(self, name):
        super().__init__(name)
        self.abilities = {'Attack': 5, 'Defence': 10, 'Speed': 4}
        self.shield_up_attack = False
        self.turn_counter = 0
        self.max_hp = 50
        self.hp = self.max_hp

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

    def turn(self, target_list):
        self.turn_counter += 1
        target = self.auto_select(target_list)
        if target is None:
            return

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

    def turn(self, target_list):
        self.turn_counter += 1
        target = self.auto_select(target_list)
        if target is None:
            return

        if self.turn_counter % 4 == 1:
            self.attack(target)
        else:
            self.power_shot(target)

class Fighter(Creature):
    def __init__(self, name):
        super().__init__(name, max_hp=50)
        self.abilities = {'Attack': 5, 'Defence': 8, 'Speed': 5}
    
    def turn(self, target_list):
        target = self.auto_select(target_list)
        if target is None:
            return

        print(f"{self.name} unleashes a flurry of strikes.")
        for i in range(3):
            if i > 0:
                self.abilities['Attack'] -= 3
            self.attack(target)
            if target.hp <= 0:
                break
        self.abilities['Attack'] = 5
    
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
        self.max_hp = 80
        self.hp = self.max_hp

    def turn(self, target_list):
        self.turn_counter += 1
        target = self.auto_select(target_list)
        if target is None:
            return

        if self.turn_counter % 4 == 1:
            self.attack(target)
            self.shield_up()
        elif self.turn_counter % 4 == 0:
            self.shield_down()
            self.heavy_attack(target)
        else:
            self.attack(target)
            
class GoblinKing(Goblin, Archer):
    def __init__(self, name):
        Goblin.__init__(self, name)  
        Archer.__init__(self, name) 
        self.max_hp = 50
        self.hp = self.max_hp

    def turn(self, target_list):
        self.turn_counter += 1
        target = self.auto_select(target_list)
        if target is None:
            return

        if self.turn_counter % 4 == 1:
            self.attack(target)
        else:
            self.power_shot(target)          

class Boss(Orc):
    def __init__(self, name):
        Orc.__init__(self, name)
        self.max_hp = 200
        self.hp = self.max_hp
        self.abilities = {'Attack': 5, 'Defence': 8, 'Speed': 5}
        self.rage_mode = False

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
    
    def heavy_attack(self, target):
        if not self.rage_mode:
            self.abilities['Attack'] += 5
            self.abilities['Defence'] -= 3
            self.rage_mode = True
            print(f"{self.name} is in rage! His Attacking stats have increased by 5 hit points, but his defence has lowered by 3.")
        return super().attack(target)

    def calm_down(self):
        if self.rage_mode:
            self.abilities['Attack'] -= 5
            self.abilities['Defence'] += 3
            self.rage_mode = False
            print(f"{self.name} has cooled down. His attacking and defensive stats have been restored.")

    def turn(self, round_num, target_list):
        if self.rage_mode:
            self.calm_down()
        else:
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
        for enemy in enemies:
            damage = random.randint(10, 20) + self.abilities['Arcana'] // 2
            enemy.hp -= damage
            print(f"{enemy.name} takes {damage} damage from Fire Storm.")
        self.modify_mana(-50)

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
                
    def turn(self, allies, enemies):
        print(f"\n{self.name} (HP: {self.hp}/{self.max_hp}, Mana: {self.mana}/100) - Choose an action:")
        print("1: Attack, 2: Fire Bolt, 3: Heal, 4: Mass Heal, 5: Fire Storm")

        valid_actions = {'1': 'attack', '2': 'fire_bolt', '3': 'heal', '4': 'mass_heal', '5': 'fire_storm'}
        while True:
            action = input("Enter your action: ")
            if action in valid_actions:
                break
            print("Invalid action. Please enter a number between 1 and 5.")

        if action in ['1', '2']:
            print("Choose a target:")
            for i, enemy in enumerate(enemies):
                print(f"{i + 1}: {enemy.name} (HP: {enemy.hp}/{enemy.max_hp})")
            target_index = int(input("Enter target index: ")) - 1
            target = enemies[target_index]

        if action == '1':
            self.attack(target)
        elif action == '2':
            self.fire_bolt(target)
        elif action == '3':
            target = self.select_target(allies + [self])
            self.heal(target)
        elif action == '4':
            self.mass_heal(allies)
        elif action == '5':
            self.fire_storm(enemies)
       
class BattleSimulation:
    def __init__(self):
        self.enemies = [
            GoblinKing("Goblin King"),
            OrcGeneral("Gothmog"),
            Goblin("Goblin"),
            Orc("Orc soldier")
        ]
        
        self.allies = [
            Fighter("Boromir"),
            Archer("Legolas"),
            Warrior("Aragorn"),
        ]

        self.boss = Boss("Mighty Boss")

        self.player = Wizard("Gandalf")

        self.print_team_classes()
        
    def player_turn(self):
        print("=" * 55)
        print(f"Player: {self.player.name} HP: {self.player.hp}/{self.player.max_hp} Mana: {self.player.mana}/100")
        print("Allies:")
        for ally in self.allies:
            print(f"{ally.name} (HP: {ally.hp}/{ally.max_hp})")
        print("=" * 55)
        print("Actions. F: Attack R: Recharge Mana")
        print("Spells. 1: Heal 2: Firebolt 3: Mass Heal 4: Fire Storm")
        print("To Quit game type: Quit")
        print("=" * 55)

        while True:
            action = input("Enter action: ").lower()

            if action == 'quit':
                print("Exiting game...")
                exit()

            if action in ['f', 'r', '1', '2', '3', '4']:
                break
            else:
                print("Invalid input. Please choose a valid action.")

        if action == 'f':
            target = self.player.select_target(self.enemies)
            if target:
                self.player.attack(target)
        elif action == 'r':
            self.player.recharge()
        elif action == '1':
            target = self.player.select_target(self.allies + [self.player])
            if target:
                self.player.heal(target)
        elif action == '2':
            target = self.player.select_target(self.enemies)
            if target:
                self.player.fire_bolt(target)
        elif action == '3':
            self.player.mass_heal(self.allies)
        elif action == '4':
            self.player.fire_storm(self.enemies)
        
    def display_health_status(self):
        print("\nCurrent Health Status:")
        print("Allies:")
        for ally in self.allies:
            print(f"{ally.name} (HP: {ally.hp}/{ally.max_hp})")

        print("\nEnemies:")
        for enemy in self.enemies:
            print(f"{enemy.name} (HP: {enemy.hp}/{enemy.max_hp})")
        print("=" * 30)
    
    def print_team_classes(self):
        print("Allies:")
        for ally in self.allies:
            print(f" - {ally.name} ({ally.__class__.__name__})")
        
        print("\nEnemies:")
        for enemy in self.enemies:
            print(f" - {enemy.name} ({enemy.__class__.__name__})")
        print(f" - {self.boss.name} ({self.boss.__class__.__name__})")
        
        print("\nPlayer:")
        print(f" - {self.player.name} ({self.player.__class__.__name__})")
        print("=" * 30)

    def start(self):
        round_number = 1
        boss_added = False

        while True:
            print(f"\n--- Round {round_number} begins ---")

            creatures_in_battle = self.allies + self.enemies + [self.player]
            creatures_in_battle.sort(key=lambda creature: creature.abilities['Speed'], reverse=True)

            for creature in creatures_in_battle:
                if creature.hp <= 0:
                    continue

                if creature is self.player:
                    self.player.turn(self.allies, self.enemies)
                elif creature in self.allies:
                    creature.turn(self.enemies)
                elif creature is self.boss:
                    creature.turn(round_number, self.allies)
                else:
                    creature.turn(self.allies)

                self.allies = [ally for ally in self.allies if ally.hp > 0]
                self.enemies = [enemy for enemy in self.enemies if enemy.hp > 0]

                if all(enemy.hp <= 0 for enemy in self.enemies):
                    print("Allies win!")
                    return
                if all(ally.hp <= 0 for ally in self.allies) or self.player.hp <= 0:
                    print("Enemies win!")
                    return
                
            if not boss_added and len([enemy for enemy in self.enemies if enemy.hp > 0]) <= 1:
                self.enemies.append(self.boss)
                boss_added = True
                print("The Boss has entered the battle!")

            self.display_health_status()
            print(f"--- Round {round_number} ends ---")
            round_number += 1   

battle = BattleSimulation()
battle.start()
