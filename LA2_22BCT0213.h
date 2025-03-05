/*#ifndef LA2_22BCT0213_H
#define LA2_22BCT0213_H

#include <stdlib.h>

// Physical Constants
#define ELECTRON_CHARGE 1.6e-19  // q: Charge of an electron in Coulombs

// Generate random quantum efficiency (η) between 0 and 1
static inline double generate_quantum_efficiency() {
    return (double)rand() / RAND_MAX;  // Returns value between 0 and 1
}

// Generate random photon flux (ϕ) between 1e10 and 1e14 photons/sec
static inline double generate_photon_flux() {
    double min_flux = 1e10;
    double max_flux = 1e14;
    double random = (double)rand() / RAND_MAX;
    return min_flux + (random * (max_flux - min_flux));
}

// Calculate photocurrent using formula: I = q * ϕ * η
static inline double calculate_photocurrent(double quantum_efficiency, double photon_flux) {
    return ELECTRON_CHARGE * photon_flux * quantum_efficiency;
}

#endif*/
/*#ifndef LA2_22BCT0213_H
#define LA2_22BCT0213_H
#define FIRE_THRESHOLD 60.0
// Structure to represent an animal
typedef struct {
int id;
float x, y;
float heat_signature;
} Animal;
// Simulates animal movement
static inline void track_animal (Animal *animal) { 
    animal->x += (rand() % 3) 1; // Move randomly in X 
    animal->y += (rand() % 3) 1; // Move randomly in Y
    animal->heat_signature 35.0+ (rand() % 5); // 35-40°C
}
static inline float generate_rand_temperature(int x,int y)
{
    return 25.0 + (rand() % 50);
}
static inline int detect_fire(float temperature)
{
    return (temperature>=FIRE_THRESHOLD);
};
#endif*/

#ifndef LA2_22BCT0213_H
#define LA2_22BCT0213_H

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <time.h>
#include <math.h>

/* Constants */
#define GRID_WIDTH 50
#define GRID_HEIGHT 40
#define BASE_TEMPERATURE 25.0f    // Base temperature in °C
#define FIRE_THRESHOLD 60.0f      // Temperature threshold for fire detection
#define MAX_FIRES 3               // Maximum number of simultaneous fires
#define MAX_ANIMALS 10            // Maximum number of deer
#define FIRE_PROBABILITY 0.02f    // Probability of new fire starting

/* Structures */
typedef struct {
    int x;
    int y;
    float intensity;
    float spread;
} FireSpot;

typedef struct {
    int x;
    int y;
    float direction;
} Animal;

typedef struct {
    float temperature_grid[GRID_HEIGHT][GRID_WIDTH];  // CCD thermal sensor data
    float animal_grid[GRID_HEIGHT][GRID_WIDTH];       // AFIR sensor data
    FireSpot fire_spots[MAX_FIRES];                   // Fire hotspots
    int fire_count;
    Animal deer[MAX_ANIMALS];                         // Deer only
    int deer_count;
    float deer_heat_signature;
    bool fire_alert;
} MonitoringSystem;

/* Function Prototypes */
void initializeSystem(MonitoringSystem *system);
void updateTemperatureGrid(MonitoringSystem *system);
void startFire(MonitoringSystem *system);
void updateFires(MonitoringSystem *system);
void updateAnimals(MonitoringSystem *system);
void updateAnimalGrid(MonitoringSystem *system);
void generateAlert(MonitoringSystem *system, char *alert_message, size_t size);
void printSystemState(MonitoringSystem *system);
void saveHeatmapToFile(float grid[GRID_HEIGHT][GRID_WIDTH], const char* filename);

/* Implementation */

// Initialize the monitoring system
void initializeSystem(MonitoringSystem *system) {
    int i, j;
    
    // Seed random number generator
    srand((unsigned int)time(NULL));
    
    // Initialize temperature grid with base temperature
    for (i = 0; i < GRID_HEIGHT; i++) {
        for (j = 0; j < GRID_WIDTH; j++) {
            system->temperature_grid[i][j] = BASE_TEMPERATURE;
            system->animal_grid[i][j] = 0.0f;
        }
    }
    
    // Initialize fire spots
    system->fire_count = 0;
    
    // Initialize alert status
    system->fire_alert = false;
    
    // Initialize deer data
    system->deer_count = 5;
    system->deer_heat_signature = 38.0f;
    
    // Initialize deer positions
    for (i = 0; i < system->deer_count; i++) {
        system->deer[i].x = rand() % GRID_WIDTH;
        system->deer[i].y = rand() % GRID_HEIGHT;
        system->deer[i].direction = ((float)rand() / RAND_MAX) * 2.0f * M_PI;
    }
}

// Update temperature grid with diffusion effects
void updateTemperatureGrid(MonitoringSystem *system) {
    float new_grid[GRID_HEIGHT][GRID_WIDTH];
    int i, j, ki, kj, ni, nj;
    float kernel[3][3] = {
        {0.1f, 0.15f, 0.1f},
        {0.15f, 0.0f, 0.15f},
        {0.1f, 0.15f, 0.1f}
    };
    
    // Copy current grid
    for (i = 0; i < GRID_HEIGHT; i++) {
        for (j = 0; j < GRID_WIDTH; j++) {
            new_grid[i][j] = system->temperature_grid[i][j];
        }
    }
    
    // Apply diffusion to inner cells
    for (i = 1; i < GRID_HEIGHT - 1; i++) {
        for (j = 1; j < GRID_WIDTH - 1; j++) {
            float temp_sum = 0.0f;
            
            // Apply kernel
            for (ki = 0; ki < 3; ki++) {
                for (kj = 0; kj < 3; kj++) {
                    ni = i + ki - 1;
                    nj = j + kj - 1;
                    temp_sum += system->temperature_grid[ni][nj] * kernel[ki][kj];
                }
            }
            
            // Add natural variation
            new_grid[i][j] += temp_sum + ((float)rand() / RAND_MAX) * 0.2f - 0.1f;
        }
    }
    
    // Limit temperature to natural range (20-100°C)
    for (i = 0; i < GRID_HEIGHT; i++) {
        for (j = 0; j < GRID_WIDTH; j++) {
            if (new_grid[i][j] < 20.0f) new_grid[i][j] = 20.0f;
            if (new_grid[i][j] > 100.0f) new_grid[i][j] = 100.0f;
            
            // Update system grid
            system->temperature_grid[i][j] = new_grid[i][j];
        }
    }
}

// Randomly start a new fire if probability check passes
void startFire(MonitoringSystem *system) {
    if ((float)rand() / RAND_MAX < FIRE_PROBABILITY && system->fire_count < MAX_FIRES) {
        int x = rand() % GRID_WIDTH;
        int y = rand() % GRID_HEIGHT;
        float intensity = 65.0f + ((float)rand() / RAND_MAX) * 25.0f;  // 65-90°C
        
        // Add new fire
        system->fire_spots[system->fire_count].x = x;
        system->fire_spots[system->fire_count].y = y;
        system->fire_spots[system->fire_count].intensity = intensity;
        system->fire_spots[system->fire_count].spread = 1.0f;
        system->fire_count++;
        
        printf("New fire started at (%d, %d) with intensity %.1f°C\n", x, y, intensity);
    }
}

// Update existing fires (spread and intensity)
void updateFires(MonitoringSystem *system) {
    int f, i, j;
    int x, y, spread;
    float dist, temp_increase;
    
    for (f = 0; f < system->fire_count; f++) {
        // Increase fire spread
        system->fire_spots[f].spread += 0.1f;
        if (system->fire_spots[f].spread > 7.0f) {
            system->fire_spots[f].spread = 7.0f;
        }
        
        // Apply fire temperature to surrounding area
        x = (int)system->fire_spots[f].x;
        y = (int)system->fire_spots[f].y;
        spread = (int)system->fire_spots[f].spread;
        
        for (i = fmax(0, y - spread); i < fmin(GRID_HEIGHT, y + spread + 1); i++) {
            for (j = fmax(0, x - spread); j < fmin(GRID_WIDTH, x + spread + 1); j++) {
                dist = sqrt(pow(j - x, 2) + pow(i - y, 2));
                
                if (dist <= system->fire_spots[f].spread) {
                    // Temperature decreases with distance from center
                    temp_increase = system->fire_spots[f].intensity * exp(-0.3 * dist);
                    
                    // Update temperature if higher than current
                    if (temp_increase > system->temperature_grid[i][j]) {
                        system->temperature_grid[i][j] = temp_increase;
                    }
                }
            }
        }
    }
}

// Update animal (deer) positions with realistic movement patterns
void updateAnimals(MonitoringSystem *system) {
    int i, f;
    float dx, dy, dist, angle;
    
    for (i = 0; i < system->deer_count; i++) {
        // Change direction occasionally
        if ((float)rand() / RAND_MAX < 0.1f) {
            system->deer[i].direction += ((float)rand() / RAND_MAX * M_PI / 2.0f) - M_PI / 4.0f;
        }
        
        // Move in current direction
        dx = 0.3f * cos(system->deer[i].direction);
        dy = 0.3f * sin(system->deer[i].direction);
        
        // Update position with boundary checking
        system->deer[i].x = fmax(0, fmin(GRID_WIDTH - 1, system->deer[i].x + dx));
        system->deer[i].y = fmax(0, fmin(GRID_HEIGHT - 1, system->deer[i].y + dy));
        
        // Deer avoid fire areas
        for (f = 0; f < system->fire_count; f++) {
            dist = sqrt(pow(system->deer[i].x - system->fire_spots[f].x, 2) + 
                       pow(system->deer[i].y - system->fire_spots[f].y, 2));
            
            if (dist < 10.0f) {  // If deer is close to fire
                // Move away from fire
                angle = atan2(system->deer[i].y - system->fire_spots[f].y, 
                             system->deer[i].x - system->fire_spots[f].x);
                system->deer[i].direction = angle;
            }
        }
    }
}

// Update animal grid based on deer positions
void updateAnimalGrid(MonitoringSystem *system) {
    int i, j, a, x, y;
    float heat_sig, dist, intensity;
    const float spread = 2.0f;
    
    // Reset animal grid
    for (i = 0; i < GRID_HEIGHT; i++) {
        for (j = 0; j < GRID_WIDTH; j++) {
            system->animal_grid[i][j] = 0.0f;
        }
    }
    
    // Update grid based on deer positions
    for (a = 0; a < system->deer_count; a++) {
        x = (int)system->deer[a].x;
        y = (int)system->deer[a].y;
        heat_sig = system->deer_heat_signature;
        
        for (i = fmax(0, y - (int)spread); i < fmin(GRID_HEIGHT, y + (int)spread + 1); i++) {
            for (j = fmax(0, x - (int)spread); j < fmin(GRID_WIDTH, x + (int)spread + 1); j++) {
                dist = sqrt(pow(j - x, 2) + pow(i - y, 2));
                
                if (dist <= spread) {
                    intensity = heat_sig * exp(-0.5 * dist);
                    
                    if (intensity > system->animal_grid[i][j]) {
                        system->animal_grid[i][j] = intensity;
                    }
                }
            }
        }
    }
}

// Generate alert messages based on system state
void generateAlert(MonitoringSystem *system, char *alert_message, size_t size) {
    float max_temp = 0.0f;
    int max_x = 0, max_y = 0;
    int i, j;
    
    // Find maximum temperature
    for (i = 0; i < GRID_HEIGHT; i++) {
        for (j = 0; j < GRID_WIDTH; j++) {
            if (system->temperature_grid[i][j] > max_temp) {
                max_temp = system->temperature_grid[i][j];
                max_y = i;
                max_x = j;
            }
        }
    }
    
    // Set fire alert if temperature exceeds threshold
    if (max_temp > FIRE_THRESHOLD) {
        system->fire_alert = true;
    }
    
    // Generate alert message
    if (system->fire_alert) {
        snprintf(alert_message, size, 
                "⚠️ FIRE ALERT! Detected temperature of %.1f°C at coordinates (%d, %d).", 
                max_temp, max_x, max_y);
        
        // If temperature drops, reset alert
        if (max_temp < 55.0f) {
            system->fire_alert = false;
        }
    } else {
        strncpy(alert_message, "System operational - No alerts active", size);
    }
}

// Print current system state
void printSystemState(MonitoringSystem *system) {
    char timestamp[30];
    char alert_message[200];
    time_t now = time(NULL);
    struct tm *t = localtime(&now);
    int i;
    
    // Format timestamp
    strftime(timestamp, sizeof(timestamp), "%Y-%m-%d %H:%M:%S", t);
    
    // Generate alert message
    generateAlert(system, alert_message, sizeof(alert_message));
    
    // Print system status
    printf("\n=== Wildlife Monitoring System Status ===\n");
    printf("Timestamp: %s\n", timestamp);
    printf("Alert: %s\n", alert_message);
    
    // Print fire spots info
    printf("\nActive fires: %d\n", system->fire_count);
    for (i = 0; i < system->fire_count; i++) {
        printf("  Fire %d: Position (%d, %d), Intensity: %.1f°C, Spread: %.1f\n",
               i + 1, 
               (int)system->fire_spots[i].x, 
               (int)system->fire_spots[i].y,
               system->fire_spots[i].intensity,
               system->fire_spots[i].spread);
    }
    
    // Print deer count
    printf("\nDeer count: %d individuals\n", system->deer_count);
    
    printf("=======================================\n");
}

// Save heatmap data to file (for external visualization)
void saveHeatmapToFile(float grid[GRID_HEIGHT][GRID_WIDTH], const char* filename) {
    FILE *file = fopen("wildlife.csv", "w");
    int i, j;
    
    if (file == NULL) {
        printf("Error opening file %s\n", filename);
        return;
    }
    
    // Write grid dimensions
    fprintf(file, "%d %d\n", GRID_HEIGHT, GRID_WIDTH);
    
    // Write grid data
    for (i = 0; i < GRID_HEIGHT; i++) {
        for (j = 0; j < GRID_WIDTH; j++) {
            fprintf(file, "%.2f ", grid[i][j]);
        }
        fprintf(file, "\n");
    }
    
    fclose(file);
}

#endif