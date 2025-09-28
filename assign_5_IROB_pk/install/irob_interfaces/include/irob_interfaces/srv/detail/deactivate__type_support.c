// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from irob_interfaces:srv/Deactivate.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "irob_interfaces/srv/detail/deactivate__rosidl_typesupport_introspection_c.h"
#include "irob_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "irob_interfaces/srv/detail/deactivate__functions.h"
#include "irob_interfaces/srv/detail/deactivate__struct.h"


#ifdef __cplusplus
extern "C"
{
#endif

void Deactivate_Request__rosidl_typesupport_introspection_c__Deactivate_Request_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  irob_interfaces__srv__Deactivate_Request__init(message_memory);
}

void Deactivate_Request__rosidl_typesupport_introspection_c__Deactivate_Request_fini_function(void * message_memory)
{
  irob_interfaces__srv__Deactivate_Request__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember Deactivate_Request__rosidl_typesupport_introspection_c__Deactivate_Request_message_member_array[1] = {
  {
    "structure_needs_at_least_one_member",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(irob_interfaces__srv__Deactivate_Request, structure_needs_at_least_one_member),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers Deactivate_Request__rosidl_typesupport_introspection_c__Deactivate_Request_message_members = {
  "irob_interfaces__srv",  // message namespace
  "Deactivate_Request",  // message name
  1,  // number of fields
  sizeof(irob_interfaces__srv__Deactivate_Request),
  Deactivate_Request__rosidl_typesupport_introspection_c__Deactivate_Request_message_member_array,  // message members
  Deactivate_Request__rosidl_typesupport_introspection_c__Deactivate_Request_init_function,  // function to initialize message memory (memory has to be allocated)
  Deactivate_Request__rosidl_typesupport_introspection_c__Deactivate_Request_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t Deactivate_Request__rosidl_typesupport_introspection_c__Deactivate_Request_message_type_support_handle = {
  0,
  &Deactivate_Request__rosidl_typesupport_introspection_c__Deactivate_Request_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_irob_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, irob_interfaces, srv, Deactivate_Request)() {
  if (!Deactivate_Request__rosidl_typesupport_introspection_c__Deactivate_Request_message_type_support_handle.typesupport_identifier) {
    Deactivate_Request__rosidl_typesupport_introspection_c__Deactivate_Request_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &Deactivate_Request__rosidl_typesupport_introspection_c__Deactivate_Request_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "irob_interfaces/srv/detail/deactivate__rosidl_typesupport_introspection_c.h"
// already included above
// #include "irob_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "irob_interfaces/srv/detail/deactivate__functions.h"
// already included above
// #include "irob_interfaces/srv/detail/deactivate__struct.h"


// Include directives for member types
// Member `message`
#include "rosidl_runtime_c/string_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void Deactivate_Response__rosidl_typesupport_introspection_c__Deactivate_Response_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  irob_interfaces__srv__Deactivate_Response__init(message_memory);
}

void Deactivate_Response__rosidl_typesupport_introspection_c__Deactivate_Response_fini_function(void * message_memory)
{
  irob_interfaces__srv__Deactivate_Response__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember Deactivate_Response__rosidl_typesupport_introspection_c__Deactivate_Response_message_member_array[2] = {
  {
    "success",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(irob_interfaces__srv__Deactivate_Response, success),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "message",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(irob_interfaces__srv__Deactivate_Response, message),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers Deactivate_Response__rosidl_typesupport_introspection_c__Deactivate_Response_message_members = {
  "irob_interfaces__srv",  // message namespace
  "Deactivate_Response",  // message name
  2,  // number of fields
  sizeof(irob_interfaces__srv__Deactivate_Response),
  Deactivate_Response__rosidl_typesupport_introspection_c__Deactivate_Response_message_member_array,  // message members
  Deactivate_Response__rosidl_typesupport_introspection_c__Deactivate_Response_init_function,  // function to initialize message memory (memory has to be allocated)
  Deactivate_Response__rosidl_typesupport_introspection_c__Deactivate_Response_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t Deactivate_Response__rosidl_typesupport_introspection_c__Deactivate_Response_message_type_support_handle = {
  0,
  &Deactivate_Response__rosidl_typesupport_introspection_c__Deactivate_Response_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_irob_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, irob_interfaces, srv, Deactivate_Response)() {
  if (!Deactivate_Response__rosidl_typesupport_introspection_c__Deactivate_Response_message_type_support_handle.typesupport_identifier) {
    Deactivate_Response__rosidl_typesupport_introspection_c__Deactivate_Response_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &Deactivate_Response__rosidl_typesupport_introspection_c__Deactivate_Response_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "irob_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "irob_interfaces/srv/detail/deactivate__rosidl_typesupport_introspection_c.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/service_introspection.h"

// this is intentionally not const to allow initialization later to prevent an initialization race
static rosidl_typesupport_introspection_c__ServiceMembers irob_interfaces__srv__detail__deactivate__rosidl_typesupport_introspection_c__Deactivate_service_members = {
  "irob_interfaces__srv",  // service namespace
  "Deactivate",  // service name
  // these two fields are initialized below on the first access
  NULL,  // request message
  // irob_interfaces__srv__detail__deactivate__rosidl_typesupport_introspection_c__Deactivate_Request_message_type_support_handle,
  NULL  // response message
  // irob_interfaces__srv__detail__deactivate__rosidl_typesupport_introspection_c__Deactivate_Response_message_type_support_handle
};

static rosidl_service_type_support_t irob_interfaces__srv__detail__deactivate__rosidl_typesupport_introspection_c__Deactivate_service_type_support_handle = {
  0,
  &irob_interfaces__srv__detail__deactivate__rosidl_typesupport_introspection_c__Deactivate_service_members,
  get_service_typesupport_handle_function,
};

// Forward declaration of request/response type support functions
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, irob_interfaces, srv, Deactivate_Request)();

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, irob_interfaces, srv, Deactivate_Response)();

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_irob_interfaces
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, irob_interfaces, srv, Deactivate)() {
  if (!irob_interfaces__srv__detail__deactivate__rosidl_typesupport_introspection_c__Deactivate_service_type_support_handle.typesupport_identifier) {
    irob_interfaces__srv__detail__deactivate__rosidl_typesupport_introspection_c__Deactivate_service_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  rosidl_typesupport_introspection_c__ServiceMembers * service_members =
    (rosidl_typesupport_introspection_c__ServiceMembers *)irob_interfaces__srv__detail__deactivate__rosidl_typesupport_introspection_c__Deactivate_service_type_support_handle.data;

  if (!service_members->request_members_) {
    service_members->request_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, irob_interfaces, srv, Deactivate_Request)()->data;
  }
  if (!service_members->response_members_) {
    service_members->response_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, irob_interfaces, srv, Deactivate_Response)()->data;
  }

  return &irob_interfaces__srv__detail__deactivate__rosidl_typesupport_introspection_c__Deactivate_service_type_support_handle;
}
