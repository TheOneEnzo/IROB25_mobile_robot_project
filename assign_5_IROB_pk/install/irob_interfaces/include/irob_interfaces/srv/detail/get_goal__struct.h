// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from irob_interfaces:srv/GetGoal.idl
// generated code does not contain a copyright notice

#ifndef IROB_INTERFACES__SRV__DETAIL__GET_GOAL__STRUCT_H_
#define IROB_INTERFACES__SRV__DETAIL__GET_GOAL__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Struct defined in srv/GetGoal in the package irob_interfaces.
typedef struct irob_interfaces__srv__GetGoal_Request
{
  uint8_t structure_needs_at_least_one_member;
} irob_interfaces__srv__GetGoal_Request;

// Struct for a sequence of irob_interfaces__srv__GetGoal_Request.
typedef struct irob_interfaces__srv__GetGoal_Request__Sequence
{
  irob_interfaces__srv__GetGoal_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} irob_interfaces__srv__GetGoal_Request__Sequence;


// Constants defined in the message

// Struct defined in srv/GetGoal in the package irob_interfaces.
typedef struct irob_interfaces__srv__GetGoal_Response
{
  double goal_x;
  double goal_y;
} irob_interfaces__srv__GetGoal_Response;

// Struct for a sequence of irob_interfaces__srv__GetGoal_Response.
typedef struct irob_interfaces__srv__GetGoal_Response__Sequence
{
  irob_interfaces__srv__GetGoal_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} irob_interfaces__srv__GetGoal_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // IROB_INTERFACES__SRV__DETAIL__GET_GOAL__STRUCT_H_
