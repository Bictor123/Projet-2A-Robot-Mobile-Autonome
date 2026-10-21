$fn = 48;

// All dimensions are in millimetres. Confirm the hole positions against the
// actual motors and caster before printing.
chassis_length = 180;
chassis_width = 140;
plate_thickness = 4;
corner_radius = 10;

motor_y = 52;
motor_hole_spacing = 36;
motor_slot_length = 10;
motor_hole_diameter = 3.4;

caster_x = 62;
caster_hole_spacing = 24;
caster_hole_diameter = 4.5;

pi_center_x = -30;
pi_hole_spacing_x = 58;
pi_hole_spacing_y = 49;
pi_hole_diameter = 2.8;

battery_slot_x = [-60, 15];
battery_slot_y = 16;
battery_slot_length = 20;
battery_slot_width = 5;

assert(chassis_length > 2 * corner_radius);
assert(chassis_width > 2 * corner_radius);
assert(2 * abs(motor_y) < chassis_width);
assert(abs(caster_x) < chassis_length / 2);

module rounded_rectangle_2d(length, width, radius) {
    hull() {
        for (x = [-length / 2 + radius, length / 2 - radius])
            for (y = [-width / 2 + radius, width / 2 - radius])
                translate([x, y]) circle(r = radius);
    }
}

module slot_2d(length, width) {
    hull() {
        translate([-(length - width) / 2, 0]) circle(d = width);
        translate([(length - width) / 2, 0]) circle(d = width);
    }
}

module through_hole(x, y, diameter) {
    translate([x, y, -1])
        cylinder(h = plate_thickness + 2, d = diameter);
}

difference() {
    linear_extrude(height = plate_thickness)
        rounded_rectangle_2d(chassis_length, chassis_width, corner_radius);

    // Slotted mounting points for the two drive motors.
    for (side = [-1, 1])
        for (offset = [-motor_hole_spacing / 2, motor_hole_spacing / 2])
            translate([offset, side * motor_y, -1])
                linear_extrude(height = plate_thickness + 2)
                    slot_2d(motor_slot_length, motor_hole_diameter);

    // Four adjustable mounting points for a ball caster at the front.
    for (x = [-caster_hole_spacing / 2, caster_hole_spacing / 2])
        for (y = [-caster_hole_spacing / 2, caster_hole_spacing / 2])
            translate([caster_x + x, y, -1])
                linear_extrude(height = plate_thickness + 2)
                    slot_2d(caster_hole_diameter + 1, caster_hole_diameter);

    // Standard Raspberry Pi mounting pattern.
    for (x = [-pi_hole_spacing_x / 2, pi_hole_spacing_x / 2])
        for (y = [-pi_hole_spacing_y / 2, pi_hole_spacing_y / 2])
            through_hole(pi_center_x + x, y, pi_hole_diameter);

    // Slots for two reusable battery straps.
    for (x = battery_slot_x)
        for (y = [-battery_slot_y, battery_slot_y])
            translate([x, y, -1])
                linear_extrude(height = plate_thickness + 2)
                    slot_2d(battery_slot_length, battery_slot_width);
}
