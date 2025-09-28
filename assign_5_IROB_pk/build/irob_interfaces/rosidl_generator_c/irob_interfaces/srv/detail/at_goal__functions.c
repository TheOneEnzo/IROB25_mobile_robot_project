// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from irob_interfaces:srv/AtGoal.idl
// generated code does not contain a copyright notice
#include "irob_interfaces/srv/detail/at_goal__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"

bool
irob_interfaces__srv__AtGoal_Request__init(irob_interfaces__srv__AtGoal_Request * msg)
{
  if (!msg) {
    return false;
  }
  // structure_needs_at_least_one_member
  return true;
}

void
irob_interfaces__srv__AtGoal_Request__fini(irob_interfaces__srv__AtGoal_Request * msg)
{
  if (!msg) {
    return;
  }
  // structure_needs_at_least_one_member
}

bool
irob_interfaces__srv__AtGoal_Request__are_equal(const irob_interfaces__srv__AtGoal_Request * lhs, const irob_interfaces__srv__AtGoal_Request * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // structure_needs_at_least_one_member
  if (lhs->structure_needs_at_least_one_member != rhs->structure_needs_at_least_one_member) {
    return false;
  }
  return true;
}

bool
irob_interfaces__srv__AtGoal_Request__copy(
  const irob_interfaces__srv__AtGoal_Request * input,
  irob_interfaces__srv__AtGoal_Request * output)
{
  if (!input || !output) {
    return false;
  }
  // structure_needs_at_least_one_member
  output->structure_needs_at_least_one_member = input->structure_needs_at_least_one_member;
  return true;
}

irob_interfaces__srv__AtGoal_Request *
irob_interfaces__srv__AtGoal_Request__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  irob_interfaces__srv__AtGoal_Request * msg = (irob_interfaces__srv__AtGoal_Request *)allocator.allocate(sizeof(irob_interfaces__srv__AtGoal_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(irob_interfaces__srv__AtGoal_Request));
  bool success = irob_interfaces__srv__AtGoal_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
irob_interfaces__srv__AtGoal_Request__destroy(irob_interfaces__srv__AtGoal_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    irob_interfaces__srv__AtGoal_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
irob_interfaces__srv__AtGoal_Request__Sequence__init(irob_interfaces__srv__AtGoal_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  irob_interfaces__srv__AtGoal_Request * data = NULL;

  if (size) {
    data = (irob_interfaces__srv__AtGoal_Request *)allocator.zero_allocate(size, sizeof(irob_interfaces__srv__AtGoal_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = irob_interfaces__srv__AtGoal_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        irob_interfaces__srv__AtGoal_Request__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
irob_interfaces__srv__AtGoal_Request__Sequence__fini(irob_interfaces__srv__AtGoal_Request__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      irob_interfaces__srv__AtGoal_Request__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

irob_interfaces__srv__AtGoal_Request__Sequence *
irob_interfaces__srv__AtGoal_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  irob_interfaces__srv__AtGoal_Request__Sequence * array = (irob_interfaces__srv__AtGoal_Request__Sequence *)allocator.allocate(sizeof(irob_interfaces__srv__AtGoal_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = irob_interfaces__srv__AtGoal_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
irob_interfaces__srv__AtGoal_Request__Sequence__destroy(irob_interfaces__srv__AtGoal_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    irob_interfaces__srv__AtGoal_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
irob_interfaces__srv__AtGoal_Request__Sequence__are_equal(const irob_interfaces__srv__AtGoal_Request__Sequence * lhs, const irob_interfaces__srv__AtGoal_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!irob_interfaces__srv__AtGoal_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
irob_interfaces__srv__AtGoal_Request__Sequence__copy(
  const irob_interfaces__srv__AtGoal_Request__Sequence * input,
  irob_interfaces__srv__AtGoal_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(irob_interfaces__srv__AtGoal_Request);
    irob_interfaces__srv__AtGoal_Request * data =
      (irob_interfaces__srv__AtGoal_Request *)realloc(output->data, allocation_size);
    if (!data) {
      return false;
    }
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!irob_interfaces__srv__AtGoal_Request__init(&data[i])) {
        /* free currently allocated and return false */
        for (; i-- > output->capacity; ) {
          irob_interfaces__srv__AtGoal_Request__fini(&data[i]);
        }
        free(data);
        return false;
      }
    }
    output->data = data;
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!irob_interfaces__srv__AtGoal_Request__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `message`
#include "rosidl_runtime_c/string_functions.h"

bool
irob_interfaces__srv__AtGoal_Response__init(irob_interfaces__srv__AtGoal_Response * msg)
{
  if (!msg) {
    return false;
  }
  // success
  // message
  if (!rosidl_runtime_c__String__init(&msg->message)) {
    irob_interfaces__srv__AtGoal_Response__fini(msg);
    return false;
  }
  return true;
}

void
irob_interfaces__srv__AtGoal_Response__fini(irob_interfaces__srv__AtGoal_Response * msg)
{
  if (!msg) {
    return;
  }
  // success
  // message
  rosidl_runtime_c__String__fini(&msg->message);
}

bool
irob_interfaces__srv__AtGoal_Response__are_equal(const irob_interfaces__srv__AtGoal_Response * lhs, const irob_interfaces__srv__AtGoal_Response * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // success
  if (lhs->success != rhs->success) {
    return false;
  }
  // message
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->message), &(rhs->message)))
  {
    return false;
  }
  return true;
}

bool
irob_interfaces__srv__AtGoal_Response__copy(
  const irob_interfaces__srv__AtGoal_Response * input,
  irob_interfaces__srv__AtGoal_Response * output)
{
  if (!input || !output) {
    return false;
  }
  // success
  output->success = input->success;
  // message
  if (!rosidl_runtime_c__String__copy(
      &(input->message), &(output->message)))
  {
    return false;
  }
  return true;
}

irob_interfaces__srv__AtGoal_Response *
irob_interfaces__srv__AtGoal_Response__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  irob_interfaces__srv__AtGoal_Response * msg = (irob_interfaces__srv__AtGoal_Response *)allocator.allocate(sizeof(irob_interfaces__srv__AtGoal_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(irob_interfaces__srv__AtGoal_Response));
  bool success = irob_interfaces__srv__AtGoal_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
irob_interfaces__srv__AtGoal_Response__destroy(irob_interfaces__srv__AtGoal_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    irob_interfaces__srv__AtGoal_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
irob_interfaces__srv__AtGoal_Response__Sequence__init(irob_interfaces__srv__AtGoal_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  irob_interfaces__srv__AtGoal_Response * data = NULL;

  if (size) {
    data = (irob_interfaces__srv__AtGoal_Response *)allocator.zero_allocate(size, sizeof(irob_interfaces__srv__AtGoal_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = irob_interfaces__srv__AtGoal_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        irob_interfaces__srv__AtGoal_Response__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
irob_interfaces__srv__AtGoal_Response__Sequence__fini(irob_interfaces__srv__AtGoal_Response__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      irob_interfaces__srv__AtGoal_Response__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

irob_interfaces__srv__AtGoal_Response__Sequence *
irob_interfaces__srv__AtGoal_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  irob_interfaces__srv__AtGoal_Response__Sequence * array = (irob_interfaces__srv__AtGoal_Response__Sequence *)allocator.allocate(sizeof(irob_interfaces__srv__AtGoal_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = irob_interfaces__srv__AtGoal_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
irob_interfaces__srv__AtGoal_Response__Sequence__destroy(irob_interfaces__srv__AtGoal_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    irob_interfaces__srv__AtGoal_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
irob_interfaces__srv__AtGoal_Response__Sequence__are_equal(const irob_interfaces__srv__AtGoal_Response__Sequence * lhs, const irob_interfaces__srv__AtGoal_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!irob_interfaces__srv__AtGoal_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
irob_interfaces__srv__AtGoal_Response__Sequence__copy(
  const irob_interfaces__srv__AtGoal_Response__Sequence * input,
  irob_interfaces__srv__AtGoal_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(irob_interfaces__srv__AtGoal_Response);
    irob_interfaces__srv__AtGoal_Response * data =
      (irob_interfaces__srv__AtGoal_Response *)realloc(output->data, allocation_size);
    if (!data) {
      return false;
    }
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!irob_interfaces__srv__AtGoal_Response__init(&data[i])) {
        /* free currently allocated and return false */
        for (; i-- > output->capacity; ) {
          irob_interfaces__srv__AtGoal_Response__fini(&data[i]);
        }
        free(data);
        return false;
      }
    }
    output->data = data;
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!irob_interfaces__srv__AtGoal_Response__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
