// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from irob_interfaces:srv/AtGoal.idl
// generated code does not contain a copyright notice

#ifndef IROB_INTERFACES__SRV__DETAIL__AT_GOAL__STRUCT_H_
#define IROB_INTERFACES__SRV__DETAIL__AT_GOAL__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Struct defined in srv/AtGoal in the package irob_interfaces.
typedef struct irob_interfaces__srv__AtGoal_Request
{
  uint8_t structure_needs_at_least_one_member;
} irob_interfaces__srv__AtGoal_Request;

// Struct for a sequence of irob_interfaces__srv__AtGoal_Request.
typedef struct irob_interfaces__srv__AtGoal_Request__Sequence
{
  irob_interfaces__srv__AtGoal_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} irob_interfaces__srv__AtGoal_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'message'
#include "rosidl_runtime_c/string.h"

// Struct defined in srv/AtGoal in the package irob_interfaces.
typedef struct irob_interfaces__srv__AtGoal_Response
{
  bool success;
  rosidl_runtime_c__String message;
} irob_interfaces__srv__AtGoal_Response;

// Struct for a sequence of irob_interfaces__srv__AtGoal_Response.
typedef struct irob_interfaces__srv__AtGoal_Response__Sequence
{
  irob_interfaces__srv__AtGoal_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} irob_interfaces__srv__AtGoal_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // IROB_INTERFACES__SRV__DETAIL__AT_GOAL__STRUCT_H_
