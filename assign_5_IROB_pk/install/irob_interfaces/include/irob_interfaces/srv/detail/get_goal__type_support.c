// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from irob_interfaces:srv/GetGoal.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "irob_interfaces/srv/detail/get_goal__rosidl_typesupport_introspection_c.h"
#include "irob_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "irob_interfaces/srv/detail/get_goal__functions.h"
#include "irob_interfaces/srv/detail/get_goal__struct.h"


#ifdef __cplusplus
extern "C"
{
#endif

void GetGoal_Request__rosidl_typesupport_introspection_c__GetGoal_Request_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  irob_interfaces__srv__GetGoal_Request__init(message_memory);
}

void GetGoal_Request__rosidl_typesupport_introspection_c__GetGoal_Request_fini_function(void * message_memory)
{
  irob_interfaces__srv__GetGoal_Request__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember GetGoal_Request__rosidl_typesupport_introspection_c__GetGoal_Request_message_member_array[1] = {
  {
    "structure_needs_at_least_one_member",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(irob_interfaces__srv__GetGoal_Request, structure_needs_at_least_one_member),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers GetGoal_Request__rosidl_typesupport_introspection_c__GetGoal_Request_message_members = {
  "irob_interfaces__srv",  // message namespace
  "GetGoal_Request",  // message name
  1,  // number of fields
  sizeof(irob_interfaces__srv__GetGoal_Request),
  GetGoal_Request__rosidl_typesupport_introspection_c__GetGoal_Request_message_member_array,  // message members
  GetGoal_Request__rosidl_typesupport_introspection_c__GetGoal_Request_init_function,  // function to initialize message memory (memory has to be allocated)
  GetGoal_Request__rosidl_typesupport_introspection_c__GetGoal_Request_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t GetGoal_Request__rosidl_typesupport_introspection_c__GetGoal_Request_message_type_support_handle = {
  0,
  &GetGoal_Request__rosidl_typesupport_introspection_c__GetGoal_Request_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_irob_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, irob_interfaces, srv, GetGoal_Request)() {
  if (!GetGoal_Request__rosidl_typesupport_introspection_c__GetGoal_Request_message_type_support_handle.typesupport_identifier) {
    GetGoal_Request__rosidl_typesupport_introspection_c__GetGoal_Request_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &GetGoal_Request__rosidl_typesupport_introspection_c__GetGoal_Request_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "irob_interfaces/srv/detail/get_goal__rosidl_typesupport_introspection_c.h"
// already included above
// #include "irob_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "irob_interfaces/srv/detail/get_goal__functions.h"
// already included above
// #include "irob_interfaces/srv/detail/get_goal__struct.h"


#ifdef __cplusplus
extern "C"
{
#endif

void GetGoal_Response__rosidl_typesupport_introspection_c__GetGoal_Response_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  irob_interfaces__srv__GetGoal_Response__init(message_memory);
}

void GetGoal_Response__rosidl_typesupport_introspection_c__GetGoal_Response_fini_function(void * message_memory)
{
  irob_interfaces__srv__GetGoal_Response__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember GetGoal_Response__rosidl_typesupport_introspection_c__GetGoal_Response_message_member_array[2] = {
  {
    "goal_x",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(irob_interfaces__srv__GetGoal_Response, goal_x),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "goal_y",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(irob_interfaces__srv__GetGoal_Response, goal_y),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers GetGoal_Response__rosidl_typesupport_introspection_c__GetGoal_Response_message_members = {
  "irob_interfaces__srv",  // message namespace
  "GetGoal_Response",  // message name
  2,  // number of fields
  sizeof(irob_interfaces__srv__GetGoal_Response),
  GetGoal_Response__rosidl_typesupport_introspection_c__GetGoal_Response_message_member_array,  // message members
  GetGoal_Response__rosidl_typesupport_introspection_c__GetGoal_Response_init_function,  // function to initialize message memory (memory has to be allocated)
  GetGoal_Response__rosidl_typesupport_introspection_c__GetGoal_Response_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t GetGoal_Response__rosidl_typesupport_introspection_c__GetGoal_Response_message_type_support_handle = {
  0,
  &GetGoal_Response__rosidl_typesupport_introspection_c__GetGoal_Response_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_irob_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, irob_interfaces, srv, GetGoal_Response)() {
  if (!GetGoal_Response__rosidl_typesupport_introspection_c__GetGoal_Response_message_type_support_handle.typesupport_identifier) {
    GetGoal_Response__rosidl_typesupport_introspection_c__GetGoal_Response_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &GetGoal_Response__rosidl_typesupport_introspection_c__GetGoal_Response_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "irob_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "irob_interfaces/srv/detail/get_goal__rosidl_typesupport_introspection_c.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/service_introspection.h"

// this is intentionally not const to allow initialization later to prevent an initialization race
static rosidl_typesupport_introspection_c__ServiceMembers irob_interfaces__srv__detail__get_goal__rosidl_typesupport_introspection_c__GetGoal_service_members = {
  "irob_interfaces__srv",  // service namespace
  "GetGoal",  // service name
  // these two fields are initialized below on the first access
  NULL,  // request message
  // irob_interfaces__srv__detail__get_goal__rosidl_typesupport_introspection_c__GetGoal_Request_message_type_support_handle,
  NULL  // response message
  // irob_interfaces__srv__detail__get_goal__rosidl_typesupport_introspection_c__GetGoal_Response_message_type_support_handle
};

static rosidl_service_type_support_t irob_interfaces__srv__detail__get_goal__rosidl_typesupport_introspection_c__GetGoal_service_type_support_handle = {
  0,
  &irob_interfaces__srv__detail__get_goal__rosidl_typesupport_introspection_c__GetGoal_service_members,
  get_service_typesupport_handle_function,
};

// Forward declaration of request/response type support functions
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, irob_interfaces, srv, GetGoal_Request)();

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, irob_interfaces, srv, GetGoal_Response)();

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_irob_interfaces
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, irob_interfaces, srv, GetGoal)() {
  if (!irob_interfaces__srv__detail__get_goal__rosidl_typesupport_introspection_c__GetGoal_service_type_support_handle.typesupport_identifier) {
    irob_interfaces__srv__detail__get_goal__rosidl_typesupport_introspection_c__GetGoal_service_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  rosidl_typesupport_introspection_c__ServiceMembers * service_members =
    (rosidl_typesupport_introspection_c__ServiceMembers *)irob_interfaces__srv__detail__get_goal__rosidl_typesupport_introspection_c__GetGoal_service_type_support_handle.data;

  if (!service_members->request_members_) {
    service_members->request_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, irob_interfaces, srv, GetGoal_Request)()->data;
  }
  if (!service_members->response_members_) {
    service_members->response_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, irob_interfaces, srv, GetGoal_Response)()->data;
  }

  return &irob_interfaces__srv__detail__get_goal__rosidl_typesupport_introspection_c__GetGoal_service_type_support_handle;
}
