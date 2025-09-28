// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from irob_interfaces:srv/Activate.idl
// generated code does not contain a copyright notice

#ifndef IROB_INTERFACES__SRV__DETAIL__ACTIVATE__FUNCTIONS_H_
#define IROB_INTERFACES__SRV__DETAIL__ACTIVATE__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "irob_interfaces/msg/rosidl_generator_c__visibility_control.h"

#include "irob_interfaces/srv/detail/activate__struct.h"

/// Initialize srv/Activate message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * irob_interfaces__srv__Activate_Request
 * )) before or use
 * irob_interfaces__srv__Activate_Request__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_irob_interfaces
bool
irob_interfaces__srv__Activate_Request__init(irob_interfaces__srv__Activate_Request * msg);

/// Finalize srv/Activate message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_irob_interfaces
void
irob_interfaces__srv__Activate_Request__fini(irob_interfaces__srv__Activate_Request * msg);

/// Create srv/Activate message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * irob_interfaces__srv__Activate_Request__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_irob_interfaces
irob_interfaces__srv__Activate_Request *
irob_interfaces__srv__Activate_Request__create();

/// Destroy srv/Activate message.
/**
 * It calls
 * irob_interfaces__srv__Activate_Request__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_irob_interfaces
void
irob_interfaces__srv__Activate_Request__destroy(irob_interfaces__srv__Activate_Request * msg);

/// Check for srv/Activate message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_irob_interfaces
bool
irob_interfaces__srv__Activate_Request__are_equal(const irob_interfaces__srv__Activate_Request * lhs, const irob_interfaces__srv__Activate_Request * rhs);

/// Copy a srv/Activate message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_irob_interfaces
bool
irob_interfaces__srv__Activate_Request__copy(
  const irob_interfaces__srv__Activate_Request * input,
  irob_interfaces__srv__Activate_Request * output);

/// Initialize array of srv/Activate messages.
/**
 * It allocates the memory for the number of elements and calls
 * irob_interfaces__srv__Activate_Request__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_irob_interfaces
bool
irob_interfaces__srv__Activate_Request__Sequence__init(irob_interfaces__srv__Activate_Request__Sequence * array, size_t size);

/// Finalize array of srv/Activate messages.
/**
 * It calls
 * irob_interfaces__srv__Activate_Request__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_irob_interfaces
void
irob_interfaces__srv__Activate_Request__Sequence__fini(irob_interfaces__srv__Activate_Request__Sequence * array);

/// Create array of srv/Activate messages.
/**
 * It allocates the memory for the array and calls
 * irob_interfaces__srv__Activate_Request__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_irob_interfaces
irob_interfaces__srv__Activate_Request__Sequence *
irob_interfaces__srv__Activate_Request__Sequence__create(size_t size);

/// Destroy array of srv/Activate messages.
/**
 * It calls
 * irob_interfaces__srv__Activate_Request__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_irob_interfaces
void
irob_interfaces__srv__Activate_Request__Sequence__destroy(irob_interfaces__srv__Activate_Request__Sequence * array);

/// Check for srv/Activate message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_irob_interfaces
bool
irob_interfaces__srv__Activate_Request__Sequence__are_equal(const irob_interfaces__srv__Activate_Request__Sequence * lhs, const irob_interfaces__srv__Activate_Request__Sequence * rhs);

/// Copy an array of srv/Activate messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_irob_interfaces
bool
irob_interfaces__srv__Activate_Request__Sequence__copy(
  const irob_interfaces__srv__Activate_Request__Sequence * input,
  irob_interfaces__srv__Activate_Request__Sequence * output);

/// Initialize srv/Activate message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * irob_interfaces__srv__Activate_Response
 * )) before or use
 * irob_interfaces__srv__Activate_Response__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_irob_interfaces
bool
irob_interfaces__srv__Activate_Response__init(irob_interfaces__srv__Activate_Response * msg);

/// Finalize srv/Activate message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_irob_interfaces
void
irob_interfaces__srv__Activate_Response__fini(irob_interfaces__srv__Activate_Response * msg);

/// Create srv/Activate message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * irob_interfaces__srv__Activate_Response__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_irob_interfaces
irob_interfaces__srv__Activate_Response *
irob_interfaces__srv__Activate_Response__create();

/// Destroy srv/Activate message.
/**
 * It calls
 * irob_interfaces__srv__Activate_Response__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_irob_interfaces
void
irob_interfaces__srv__Activate_Response__destroy(irob_interfaces__srv__Activate_Response * msg);

/// Check for srv/Activate message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_irob_interfaces
bool
irob_interfaces__srv__Activate_Response__are_equal(const irob_interfaces__srv__Activate_Response * lhs, const irob_interfaces__srv__Activate_Response * rhs);

/// Copy a srv/Activate message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_irob_interfaces
bool
irob_interfaces__srv__Activate_Response__copy(
  const irob_interfaces__srv__Activate_Response * input,
  irob_interfaces__srv__Activate_Response * output);

/// Initialize array of srv/Activate messages.
/**
 * It allocates the memory for the number of elements and calls
 * irob_interfaces__srv__Activate_Response__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_irob_interfaces
bool
irob_interfaces__srv__Activate_Response__Sequence__init(irob_interfaces__srv__Activate_Response__Sequence * array, size_t size);

/// Finalize array of srv/Activate messages.
/**
 * It calls
 * irob_interfaces__srv__Activate_Response__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_irob_interfaces
void
irob_interfaces__srv__Activate_Response__Sequence__fini(irob_interfaces__srv__Activate_Response__Sequence * array);

/// Create array of srv/Activate messages.
/**
 * It allocates the memory for the array and calls
 * irob_interfaces__srv__Activate_Response__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_irob_interfaces
irob_interfaces__srv__Activate_Response__Sequence *
irob_interfaces__srv__Activate_Response__Sequence__create(size_t size);

/// Destroy array of srv/Activate messages.
/**
 * It calls
 * irob_interfaces__srv__Activate_Response__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_irob_interfaces
void
irob_interfaces__srv__Activate_Response__Sequence__destroy(irob_interfaces__srv__Activate_Response__Sequence * array);

/// Check for srv/Activate message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_irob_interfaces
bool
irob_interfaces__srv__Activate_Response__Sequence__are_equal(const irob_interfaces__srv__Activate_Response__Sequence * lhs, const irob_interfaces__srv__Activate_Response__Sequence * rhs);

/// Copy an array of srv/Activate messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_irob_interfaces
bool
irob_interfaces__srv__Activate_Response__Sequence__copy(
  const irob_interfaces__srv__Activate_Response__Sequence * input,
  irob_interfaces__srv__Activate_Response__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // IROB_INTERFACES__SRV__DETAIL__ACTIVATE__FUNCTIONS_H_
