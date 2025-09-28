// generated from rosidl_typesupport_fastrtps_c/resource/idl__type_support_c.cpp.em
// with input from irob_interfaces:srv/GetGoal.idl
// generated code does not contain a copyright notice
#include "irob_interfaces/srv/detail/get_goal__rosidl_typesupport_fastrtps_c.h"


#include <cassert>
#include <limits>
#include <string>
#include "rosidl_typesupport_fastrtps_c/identifier.h"
#include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "irob_interfaces/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "irob_interfaces/srv/detail/get_goal__struct.h"
#include "irob_interfaces/srv/detail/get_goal__functions.h"
#include "fastcdr/Cdr.h"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

// includes and forward declarations of message dependencies and their conversion functions

#if defined(__cplusplus)
extern "C"
{
#endif


// forward declare type support functions


using _GetGoal_Request__ros_msg_type = irob_interfaces__srv__GetGoal_Request;

static bool _GetGoal_Request__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const _GetGoal_Request__ros_msg_type * ros_message = static_cast<const _GetGoal_Request__ros_msg_type *>(untyped_ros_message);
  // Field name: structure_needs_at_least_one_member
  {
    cdr << ros_message->structure_needs_at_least_one_member;
  }

  return true;
}

static bool _GetGoal_Request__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  _GetGoal_Request__ros_msg_type * ros_message = static_cast<_GetGoal_Request__ros_msg_type *>(untyped_ros_message);
  // Field name: structure_needs_at_least_one_member
  {
    cdr >> ros_message->structure_needs_at_least_one_member;
  }

  return true;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_irob_interfaces
size_t get_serialized_size_irob_interfaces__srv__GetGoal_Request(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _GetGoal_Request__ros_msg_type * ros_message = static_cast<const _GetGoal_Request__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // field.name structure_needs_at_least_one_member
  {
    size_t item_size = sizeof(ros_message->structure_needs_at_least_one_member);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}

static uint32_t _GetGoal_Request__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_irob_interfaces__srv__GetGoal_Request(
      untyped_ros_message, 0));
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_irob_interfaces
size_t max_serialized_size_irob_interfaces__srv__GetGoal_Request(
  bool & full_bounded,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;
  (void)full_bounded;

  // member: structure_needs_at_least_one_member
  {
    size_t array_size = 1;

    current_alignment += array_size * sizeof(uint8_t);
  }

  return current_alignment - initial_alignment;
}

static size_t _GetGoal_Request__max_serialized_size(bool & full_bounded)
{
  return max_serialized_size_irob_interfaces__srv__GetGoal_Request(
    full_bounded, 0);
}


static message_type_support_callbacks_t __callbacks_GetGoal_Request = {
  "irob_interfaces::srv",
  "GetGoal_Request",
  _GetGoal_Request__cdr_serialize,
  _GetGoal_Request__cdr_deserialize,
  _GetGoal_Request__get_serialized_size,
  _GetGoal_Request__max_serialized_size
};

static rosidl_message_type_support_t _GetGoal_Request__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_GetGoal_Request,
  get_message_typesupport_handle_function,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, irob_interfaces, srv, GetGoal_Request)() {
  return &_GetGoal_Request__type_support;
}

#if defined(__cplusplus)
}
#endif

// already included above
// #include <cassert>
// already included above
// #include <limits>
// already included above
// #include <string>
// already included above
// #include "rosidl_typesupport_fastrtps_c/identifier.h"
// already included above
// #include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
// already included above
// #include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
// already included above
// #include "irob_interfaces/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
// already included above
// #include "irob_interfaces/srv/detail/get_goal__struct.h"
// already included above
// #include "irob_interfaces/srv/detail/get_goal__functions.h"
// already included above
// #include "fastcdr/Cdr.h"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

// includes and forward declarations of message dependencies and their conversion functions

#if defined(__cplusplus)
extern "C"
{
#endif


// forward declare type support functions


using _GetGoal_Response__ros_msg_type = irob_interfaces__srv__GetGoal_Response;

static bool _GetGoal_Response__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const _GetGoal_Response__ros_msg_type * ros_message = static_cast<const _GetGoal_Response__ros_msg_type *>(untyped_ros_message);
  // Field name: goal_x
  {
    cdr << ros_message->goal_x;
  }

  // Field name: goal_y
  {
    cdr << ros_message->goal_y;
  }

  return true;
}

static bool _GetGoal_Response__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  _GetGoal_Response__ros_msg_type * ros_message = static_cast<_GetGoal_Response__ros_msg_type *>(untyped_ros_message);
  // Field name: goal_x
  {
    cdr >> ros_message->goal_x;
  }

  // Field name: goal_y
  {
    cdr >> ros_message->goal_y;
  }

  return true;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_irob_interfaces
size_t get_serialized_size_irob_interfaces__srv__GetGoal_Response(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _GetGoal_Response__ros_msg_type * ros_message = static_cast<const _GetGoal_Response__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // field.name goal_x
  {
    size_t item_size = sizeof(ros_message->goal_x);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name goal_y
  {
    size_t item_size = sizeof(ros_message->goal_y);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}

static uint32_t _GetGoal_Response__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_irob_interfaces__srv__GetGoal_Response(
      untyped_ros_message, 0));
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_irob_interfaces
size_t max_serialized_size_irob_interfaces__srv__GetGoal_Response(
  bool & full_bounded,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;
  (void)full_bounded;

  // member: goal_x
  {
    size_t array_size = 1;

    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }
  // member: goal_y
  {
    size_t array_size = 1;

    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  return current_alignment - initial_alignment;
}

static size_t _GetGoal_Response__max_serialized_size(bool & full_bounded)
{
  return max_serialized_size_irob_interfaces__srv__GetGoal_Response(
    full_bounded, 0);
}


static message_type_support_callbacks_t __callbacks_GetGoal_Response = {
  "irob_interfaces::srv",
  "GetGoal_Response",
  _GetGoal_Response__cdr_serialize,
  _GetGoal_Response__cdr_deserialize,
  _GetGoal_Response__get_serialized_size,
  _GetGoal_Response__max_serialized_size
};

static rosidl_message_type_support_t _GetGoal_Response__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_GetGoal_Response,
  get_message_typesupport_handle_function,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, irob_interfaces, srv, GetGoal_Response)() {
  return &_GetGoal_Response__type_support;
}

#if defined(__cplusplus)
}
#endif

#include "rosidl_typesupport_fastrtps_cpp/service_type_support.h"
#include "rosidl_typesupport_cpp/service_type_support.hpp"
// already included above
// #include "rosidl_typesupport_fastrtps_c/identifier.h"
// already included above
// #include "irob_interfaces/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "irob_interfaces/srv/get_goal.h"

#if defined(__cplusplus)
extern "C"
{
#endif

static service_type_support_callbacks_t GetGoal__callbacks = {
  "irob_interfaces::srv",
  "GetGoal",
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, irob_interfaces, srv, GetGoal_Request)(),
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, irob_interfaces, srv, GetGoal_Response)(),
};

static rosidl_service_type_support_t GetGoal__handle = {
  rosidl_typesupport_fastrtps_c__identifier,
  &GetGoal__callbacks,
  get_service_typesupport_handle_function,
};

const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, irob_interfaces, srv, GetGoal)() {
  return &GetGoal__handle;
}

#if defined(__cplusplus)
}
#endif
